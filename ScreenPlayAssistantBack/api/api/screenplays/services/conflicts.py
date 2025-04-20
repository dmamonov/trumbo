from api.screenplays.models import ScreenPlay, ConflictPoint
from api.screenplays.services.prompt import LLMPrompt
from .screenplays import ScreenPlaySteps
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional
import json, re

@dataclass
class ParsedScene:
    slugline: str
    content: str
    position: int


def get_scenes_from_screenplay_content(content: str, scene_markers: Optional[List[str]] = None) -> List[ParsedScene]:
    if scene_markers is None:
        scene_markers = ['INT.', 'EXT.', 'INT/EXT.']

    # Sluglines usually include markers and are all caps; capture line with marker
    escaped = [re.escape(marker) for marker in scene_markers]
    slugline_pattern = rf".*?(?:{'|'.join(escaped)}).*"

    lines = content.splitlines()
    scenes = []
    current_slug = None
    current_content = []
    position = 0

    for line in lines:
        if re.match(slugline_pattern, line.strip(), re.IGNORECASE):
            # Save current scene if exists
            if current_slug or current_content:
                scenes.append(ParsedScene(
                    slugline=current_slug.strip() if current_slug else "UNKNOWN",
                    content="\n".join(current_content).strip(),
                    position=position
                ))
                position += 1
                current_content = []
            current_slug = line
        else:
            current_content.append(line)

    # Add final scene
    if current_slug or current_content:
        scenes.append(ParsedScene(
            slugline=current_slug.strip() if current_slug else "UNKNOWN",
            content="\n".join(current_content).strip(),
            position=position
        ))

    return scenes

def get_existing_conflicts(screenplay: ScreenPlay
        ) -> Tuple[List[ConflictPoint], Dict[Tuple, ConflictPoint], List[Dict[str, Any]]]:
    """
    Fetch all ConflictPoints for this screenplay, return:
      • queryset list  
      • dict mapping (name,intro,resolved) → model instance  
      • list of dicts for LLM context
    """
    qs = list(ConflictPoint.objects.filter(screenplay=screenplay))
    key_map = {
        (c.conflict_name, ): c
        for c in qs
    }
    ctx = []
    for c in qs:
        ctx.append({
            "conflict_name": c.conflict_name,
            "introduced_at_regex": c.introduced_at_regex,
            "resolved_at_regex": c.resolved_at_regex,
            "description": c.description,
            "criticality": c.criticality,
            "certainty": c.certainty,
            "conclusion": c.conclusion,
        })
    return qs, key_map, ctx


def prepare_llm_context(scene_text: str, existing_ctx: List[Dict[str, Any]]):
    return json.dumps({
        "scene": scene_text,
        "existing_conflicts": existing_ctx
    })


def process_scene_for_conflict_data(
    scene: ParsedScene,
    existing_keys: Dict[Tuple, ConflictPoint],
    existing_ctx: List[Dict[str, Any]]
) -> Tuple[List[Any], List[Tuple[Any, ConflictPoint]]]:
    """
    Returns two lists:
      • new_conflict_data: list of PydanticConflict objects  
      • existing_pairs: list of (PydanticConflict, ConflictPoint instance)
    """
    payload = prepare_llm_context(scene.content, existing_ctx)
    try:
        resp = ScreenPlaySteps.get_conflict_points_from_scene.execute(
            payload,
            extra_messages=[{
                "role": "user",
                "content": f"Existing conflicts: {existing_ctx}"
            }]
        )
    except Exception:
        return [], []

    new_data, existing_pairs = [], []
    for cd in resp.conflicts:
        key = (cd.conflict_name,)
        if key in existing_keys:
            existing_pairs.append((cd, existing_keys[key]))
        else:
            new_data.append(cd)
    return new_data, existing_pairs


def get_and_save_conflict_points_from_llm(screenplay: ScreenPlay):
    """
    Orchestrator: parse scenes, call LLM per scene, create/update conflicts,
    and keep context up-to-date for each call.
    """
    _, existing_keys, existing_ctx = get_existing_conflicts(screenplay)
    scenes = get_scenes_from_screenplay_content(screenplay.content)

    all_new, all_existing = [], []

    for scene in scenes:
        try:
            new_data, existing_pairs = process_scene_for_conflict_data(
                scene, existing_keys, existing_ctx
            )
        except Exception as e:
            # Handle LLM/processing failure per scene
            print(f"[ERROR] Failed to process scene at position {scene.position}: {e}")
            continue  # Skip to next scene

        # 1) CREATE new conflicts right away and add to context
        for cd in new_data:
            inst = ConflictPoint(**cd.dict(), screenplay=screenplay, start_scene_position=scene.position)
            inst.save()
            all_new.append(inst)

            key = (cd.conflict_name, )
            existing_keys[key] = inst
            existing_ctx.append(cd.dict())

        # 2) UPDATE any existing conflicts & refresh them in context
        for cd, inst in existing_pairs:
            key = (cd.conflict_name, )
            updated = False
            inst.last_updated_scene_position = scene.position
            for field, val in cd.dict().items():
                if getattr(inst, field) != val:
                    setattr(inst, field, val)
                    updated = True
            if updated:
                inst.save()
            all_existing.append(inst)

            for d in existing_ctx:
                if (d['conflict_name'], ) == key:
                    d.update(cd.dict())
                    break

    return all_new, all_existing



import re
def normalize_and_index(text):
    normalized = []
    index_map = []

    for i, c in enumerate(text):
        if c.isalnum():  # Keep only alphanumeric characters
            normalized.append(c.lower())
            index_map.append(i)
    return ''.join(normalized), index_map

def find_normalized_substring_index(full_text, search_substring):
    norm_text, index_map = normalize_and_index(full_text)
    norm_search = ''.join(c.lower() for c in search_substring if c.isalnum())

    idx = norm_text.find(norm_search)
    if idx == -1:
        return -1  # Not found
    return index_map[idx]

def get_screenplay_conflict_resolution_index(sp):
    content = sp.content
    for x in sp.conflict_points.all():
        print("A", find_normalized_substring_index(content, x.introduced_at_regex,))
        print("B", find_normalized_substring_index(content, x.resolved_at_regex,))

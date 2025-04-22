from api.screenplays.models import *
from pydantic import BaseModel as PydanticBaseModel
from typing import List
from api.screenplays.services.prompt import LLMPrompt
from dataclasses import dataclass

# Response Schemas
class HighlightSceneResponse(PydanticBaseModel):
    scenes: List[SceneHighlight.PydanticSchema]

class ConflictPointResponse(PydanticBaseModel):
    conflicts: List[ConflictPoint.PydanticSchema]

@dataclass(frozen=True)
class SceneSteps:
    show_dont_tell_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze the following scene. "
                    "Check for violations of the 'show, don’t tell' rule. "
                    "Flag any narrative exposition that could be conveyed visually or through action."
                ),
            },
        ],
        response_schema=HighlightSceneResponse
    )

    boring_scene_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": (
                    "Assess this scene for pacing issues. "
                    "Is it too long, slow, rushed, or lacking structure (setup, escalation, payoff)? "
                    "Highlight any boring or poorly paced moments."
                ),
            },
        ],
        response_schema=HighlightSceneResponse
    )

    camera_instruction_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": (
                    "Review this scene and highlight any direct camera instructions "
                    "such as 'pan', 'zoom', or 'close-up'. "
                    "Suggest immersive storytelling alternatives that avoid breaking the fourth wall."
                ),
            },
        ],
        response_schema=HighlightSceneResponse
    )

    scene_feasibility_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": (
                    "Evaluate the scene for production feasibility. "
                    "Identify any elements requiring visual effects (VFX), stunts, "
                    "complex choreography, or elaborate sets. Estimate complexity."
                ),
            },
        ],
        response_schema=HighlightSceneResponse
    )

    dead_end_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": (
                    "Determine if this scene is a narrative dead-end — "
                    "i.e., if it doesn’t contribute meaningfully to character arcs or story progression. "
                    "Highlight parts that might be trimmed or rewritten."
                ),
            },
        ],
        response_schema=HighlightSceneResponse
    )

    get_conflict_points = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze this scene for conflict dynamics. "
                    "Check whether any known conflict points are introduced, escalated, or resolved. "
                    "Do not invent conflicts — only respond based on given context."
                ),
            },
        ],
        response_schema=ConflictPointResponse
    )


def _run_and_save_scene_highlight(
    scene: Scene,
    prompt: LLMPrompt,
    check_name: str
):
    """
    Helper: Run a Scene-specific LLM prompt, then save the
    returned highlights as SceneHighlight entries tied to that Scene.
    """
    response = prompt.execute(scene.content)

    created = []
    for result in response.scenes:
        highlight = SceneHighlight.objects.create(
            scene=scene,
            screenplay=scene.screenplay,
            name=result.name,
            type=check_name,
            description=result.description,
            related_text=result.related_text,
            criticality=result.criticality,
            certainty=result.certainty,
            conclusion=result.conclusion,
        )
        created.append(highlight)
    return created


def show_dont_tell_check(scene: Scene):
    return _run_and_save_scene_highlight(
        scene,
        SceneSteps.show_dont_tell_check,
        check_name='show_dont_tell'
    )


def boring_scene_check(scene: Scene):
    return _run_and_save_scene_highlight(
        scene,
        SceneSteps.boring_scene_check,
        check_name='boring_scene'
    )


def camera_instruction_check(scene: Scene):
    return _run_and_save_scene_highlight(
        scene,
        SceneSteps.camera_instruction_check,
        check_name='camera_operation'
    )


def dead_end_check(scene: Scene):
    return _run_and_save_scene_highlight(
        scene,
        SceneSteps.dead_end_check,
        check_name='dead_end'
    )


def scene_feasibility_check(scene: Scene):
    return _run_and_save_scene_highlight(
        scene,
        SceneSteps.scene_feasibility_check,
        check_name='scene_feasibility'
    )

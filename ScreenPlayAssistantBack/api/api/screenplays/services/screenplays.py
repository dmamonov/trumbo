from api.screenplays.models import Character, ScreenPlay, SceneHighlight
from pydantic import BaseModel as PydanticBaseModel
from typing import List
from api.screenplays.services.prompt import LLMPrompt
from dataclasses import dataclass
import json

class CharactersFromPlayResponse(PydanticBaseModel):
    characters: List[Character.PydanticSchema]

class ScreenPlayResponse(PydanticBaseModel):
    screenplay: str

class HighlightSceensResponse(PydanticBaseModel):
    sceens: List[SceneHighlight.PydanticSchema]

@dataclass(frozen=True)
class ScreenPlaySteps:
    characters_from_play = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": "get all the characters from the following screen play",
            },
        ],
        response_schema=CharactersFromPlayResponse
    )
    camera_operation_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": "In the following screenplay look for the following mistake: there should not be direct operation on camera",
            },
        ],
        response_schema=HighlightSceensResponse
    )
    show_dont_tell_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": "In the following screenplay look for the following mistake: there should be no direct narration (story have to be shown, not told)",
            },
        ],
        response_schema=HighlightSceensResponse
    )
    # TODO: Semantic patch: compare two drafts and explain what the difference (not the plain diff)
    # TODO: Implement check/markup: possibility to shot a scene / requirements of visual effects in scene
    # TODO: Implement markup/extraction: continuity, progression, premise, theme, forestalling, finger-posts, preparation, anticlimax, complication, scene, catastrophe, resolution, representation, crisis, antagonist, impressionism, adjustment, peripety, irony, attack, focus, suspense, action recognition, balance, movement, orchestration, unity of opposites, static, jumping, transition, incudent (see page #16)
    boring_sceenes_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": "In the following screenplay look for the following mistake: boring sceen",
            },
        ],
        response_schema=HighlightSceensResponse
    )
    # TODO: Implement check: The audience ephatize with a character not becase they are in pain or oppressed, but because of what they are doing about it
    dead_end_check = LLMPrompt(
        messages=[
            {
                "role": "system",
                "content": "In the following screenplay look for the following mistake: highlight dead-ends (scenes not contributing to the Final)",
            },
        ],
        response_schema=HighlightSceensResponse
    )

def get_and_save_characters_from_llm(screenplay: ScreenPlay):
    # Get character data from the LLM
    characters_data = ScreenPlaySteps.characters_from_play.execute(screenplay.content)
    # Extract all character names from the LLM response
    names = [character_data.name for character_data in characters_data.characters]
    
    # Retrieve all characters from the database matching these names for the given screenplay
    existing_qs = Character.objects.filter(name__in=names, screenplay=screenplay)
    # Build a dictionary for quick lookup
    existing_by_name = {character.name: character for character in existing_qs}
    
    new_characters = []
    old_characters = []
    
    for character_data in characters_data:
        # Use character_data.dict() to convert to a dictionary
        if character_data.name in existing_by_name:
            # If the character already exists, append the existing instance
            old_characters.append(existing_by_name[character_data.name])
        else:
            # If not, create a new Character instance (not yet saved)
            new_characters.append(
                Character(**character_data.dict(), screenplay=screenplay)
            )
    
    # Bulk create new characters in one query
    created_new = Character.objects.bulk_create(new_characters)
    # Return the combination of created and already existing characters
    return list(created_new), old_characters

# api/screenplays/services/checks.py

from api.screenplays.models import ScreenPlay, SceneHighlight
from .prompt import LLMPrompt
from .screenplays import ScreenPlaySteps


def _run_and_save_highlight(
    screenplay: ScreenPlay,
    prompt: LLMPrompt,
    check_name: str
):
    """
    Helper: run the given LLMPrompt on the screenplay, then save each
    returned SceenHiglight to the DB as a SceneHighlight.
    """
    # Execute the LLM prompt against the screenplay text
    response = prompt.execute(screenplay.content)

    created = []
    for scene in response.sceens:
        # scene.title → name/label of the finding
        # scene.reason → description of why it was flagged
        # we'll use scene.title again as the 'related_text' snippet
        highlight = SceneHighlight.objects.create(
            screenplay=screenplay,
            name=scene.name,
            type=check_name,
            description=scene.description,
            related_text=scene.related_text,
            
            criticality=scene.criticality,
            certainty=scene.certainty,
            conclusion=scene.conclusion,
        )
        created.append(highlight)
    return created


def check_camera_operations(screenplay: ScreenPlay):
    """
    Finds any direct camera operations in the screenplay
    and persists them as SceneHighlight(name='camera_operation', ...).
    """
    return _run_and_save_highlight(
        screenplay,
        ScreenPlaySteps.camera_operation_check,
        check_name='camera_operation'
    )


def show_dont_tell_check(screenplay: ScreenPlay):
    """
    Flags any ‘telling’ (narration) rather than ‘showing’ and saves
    each as SceneHighlight(name='show_dont_tell', ...).
    """
    return _run_and_save_highlight(
        screenplay,
        ScreenPlaySteps.show_dont_tell_check,
        check_name='show_dont_tell'
    )


def boring_scenes_check(screenplay: ScreenPlay):
    """
    Identifies boring scenes and saves them as
    SceneHighlight(name='boring_scene', ...).
    """
    return _run_and_save_highlight(
        screenplay,
        ScreenPlaySteps.boring_sceenes_check,
        check_name='boring_scene'
    )


def dead_end_check(screenplay: ScreenPlay):
    """
    Highlights scenes that don’t contribute to the finale, saving them
    as SceneHighlight(name='dead_end', ...).
    """
    return _run_and_save_highlight(
        screenplay,
        ScreenPlaySteps.dead_end_check,
        check_name='dead_end'
    )

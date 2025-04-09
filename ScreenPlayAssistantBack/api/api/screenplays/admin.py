"""User models admin."""

# Django
from django.contrib import admin

# Models
from api.screenplays.models import *
from api.screenplays.services.screenplays import get_and_save_characters_from_llm

from django.utils.translation import ngettext
from django.contrib import messages
from django.utils.text import slugify
from datetime import datetime
from django.http import HttpResponseRedirect
import os
from django.utils.html import format_html

def export_characters_markdown(screenplay):
    """
    Generate Markdown string for characters in a screenplay and save it to a file.

    Returns:
        str: Relative path to the saved file (for building download URL).
    """
    filename = f"{slugify(screenplay.title)}-characters-{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    output_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    markdown = f"# Characters in *{screenplay.title}*\n\n"
    characters = screenplay.characters.all()

    if not characters:
        markdown += "_No characters found for this screenplay._"
    else:
        for character in characters:
            markdown += f"## {character.name}\n"
            if character.description:
                markdown += f"**Description:** {character.description}\n\n"
            if character.profile:
                markdown += f"**Profile:**\n{character.profile}\n\n"
            else:
                markdown += "_No profile provided._\n\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

    return os.path.join('exports', filename)

@admin.register(ScreenPlay)
class ScreenPlayAdmin(admin.ModelAdmin):
    list_display = ScreenPlay.Api.list
    actions = ["get_and_save_characters", "export_characters_as_markdown"]
    
    @admin.action(description="Get and Save Characters")
    def get_and_save_characters(self, request, queryset):
        for screen_play in queryset:
            created_new, old_characters = get_and_save_characters_from_llm(screen_play)
            self.message_user(
                request,
                ngettext(
                    "%d character was successfully identifeid and saved.",
                    "%d characters were successfully identifeid and saved.",
                    len(created_new),
                )
                % len(created_new),
                messages.SUCCESS,
            )
    
    @admin.action(description="Generate mark down")
    def export_characters_as_markdown(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one screenplay to export.", level=messages.WARNING)
            return

        screenplay = queryset.first()
        relative_path = export_characters_markdown(screenplay)
        file_url = f"{settings.MEDIA_URL}{relative_path}"

        self.message_user(request, format_html(f"Export complete! <a href='{file_url}' target='_blank'>Download Markdown file</a>"), level=messages.SUCCESS)
        return HttpResponseRedirect(request.get_full_path())

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = Character.Api.list

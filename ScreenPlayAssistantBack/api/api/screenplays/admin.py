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

import json
from django.conf import settings

@admin.register(ScreenPlay)
class ScreenPlayAdmin(admin.ModelAdmin):
    list_display = ScreenPlay.Api.list
    actions = ["get_and_save_characters", "export_characters_as_markdown"]
    
    @admin.action(description="Get and Save Characters")
    def get_and_save_characters(self, request, queryset):
        for screen_play in queryset:
            try:
                created_new, old_characters = get_and_save_characters_from_llm(screen_play)
            except json.decoder.JSONDecodeError:
                self.message_user(
                    request,
                    "Error Decoding agent's response",
                    messages.ERROR,
                )
                return
            self.message_user(
                request,
                ngettext(
                    "%d character was successfully identified and saved.",
                    "%d characters were successfully identified and saved.",
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
        relative_path = screenplay.export_characters_markdown()
        file_url = f"{settings.MEDIA_URL}{relative_path}"

        self.message_user(request, format_html(f"Export complete! <a href='{file_url}' target='_blank'>Download Markdown file</a>"), level=messages.SUCCESS)
        return HttpResponseRedirect(request.get_full_path())

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = Character.Api.list

"""User models admin."""

# Django
from django.contrib import admin

# Models
from api.screenplays.models import *
from api.screenplays.services.screenplays import get_and_save_characters_from_llm

from django.utils.translation import ngettext
from django.contrib import messages

@admin.register(ScreenPlay)
class ScreenPlayAdmin(admin.ModelAdmin):
    list_display = ScreenPlay.Api.list
    actions = ["get_and_save_characters"]
    
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
    
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = Character.Api.list

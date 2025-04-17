"""Screen Play models admin."""

# Django
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.conf import settings

# Models
from api.screenplays.models import ScreenPlay, Character, SceneHighlight
# Existing services
from api.screenplays.services.screenplays import get_and_save_characters_from_llm
from api.screenplays.services.corrections import save_document_embeddings, query_related_paragraph
# New check services
from api.screenplays.services.checks import (
    check_camera_operations,
    show_dont_tell_check,
    boring_scenes_check,
    dead_end_check,
)

@admin.register(ScreenPlay)
class ScreenPlayAdmin(admin.ModelAdmin):
    list_display = ScreenPlay.Api.list
    actions = [
        "get_and_save_characters",
        "export_characters_as_markdown",
        "save_embedings",
        "query_related_paragraphs",
        # new quality‐check actions
        "camera_operations_check",
        "show_dont_tell_check_action",
        "boring_scenes_check_action",
        "dead_end_check_action",
        "run_full_analysis",
        "export_failed_checks_as_markdown"
    ]
    
    @admin.action(description="Run Full LLM Analysis (quality checks)")
    def run_full_analysis(self, request, queryset):
        """
        Executes the entire pipeline for each selected screenplay:
          Run all four quality checks
        """
        for sp in queryset:
            # 1) Characters
            # try:
            #     new_chars, _old = get_and_save_characters_from_llm(sp)
            #     char_count = len(new_chars)
            # except Exception as e:
            #     self.message_user(
            #         request,
            #         f"[{sp.title}] Character extraction failed: {e}",
            #         messages.ERROR
            #     )
            #     # skip to next screenplay
            #     continue

            # 2) Quality checks
            cam_ops = check_camera_operations(sp)
            tells   = show_dont_tell_check(sp)
            boring  = boring_scenes_check(sp)
            dead    = dead_end_check(sp)

            # Aggregate & report
            self.message_user(
                request,
                format_html(
                    "<strong>{title}</strong>: "
                    "{} camera‑ops, {} show‑don’t‑tell, {} boring, {} dead‑end",
                    len(cam_ops),
                    len(tells),
                    len(boring),
                    len(dead),
                    title=sp.title
                ),
                messages.SUCCESS
            )

        # Refresh the changelist so counts are up‑to‑date
        return HttpResponseRedirect(request.get_full_path())

    @admin.action(description="Save Embeddings")
    def save_embedings(self, request, queryset):
        for screen_play in queryset:
            count, _, _ = save_document_embeddings(
                str(screen_play.created_by.id),
                screen_play.title,
                screen_play.content
            )
            self.message_user(
                request,
                ngettext(
                    "%d embedding was successfully saved.",
                    "%d embeddings were successfully saved.",
                    count,
                ) % count,
                messages.SUCCESS,
            )

    @admin.action(description="Query Related Paragraphs")
    def query_related_paragraphs(self, request, queryset):
        for screen_play in queryset:
            _results = query_related_paragraph(
                "main character appears",
                str(screen_play.created_by.id),
                screen_play.title
            )
        self.message_user(request, "Related‐paragraph queries completed.", messages.SUCCESS)

    @admin.action(description="Get and Save Characters")
    def get_and_save_characters(self, request, queryset):
        for screen_play in queryset:
            try:
                created_new, _old = get_and_save_characters_from_llm(screen_play)
                new_count = len(created_new)
                self.message_user(
                    request,
                    ngettext(
                        "%d character was successfully identified and saved.",
                        "%d characters were successfully identified and saved.",
                        new_count,
                    ) % new_count,
                    messages.SUCCESS,
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error identifying characters: {e}",
                    messages.ERROR,
                )

    @admin.action(description="Generate Markdown of Characters")
    def export_characters_as_markdown(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Please select exactly one screenplay to export.",
                level=messages.WARNING
            )
            return
        screenplay = queryset.first()
        relative_path = screenplay.export_characters_markdown()
        file_url = f"{settings.MEDIA_URL}{relative_path}"
        self.message_user(
            request,
            format_html(
                "Export complete! <a href='{}' target='_blank'>Download Markdown file</a>",
                file_url
            ),
            level=messages.SUCCESS
        )
        return HttpResponseRedirect(request.get_full_path())
    
    @admin.action(description="Generate MD File for Failed Checks")
    def export_failed_checks_as_markdown(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Please select exactly one screenplay to export.",
                level=messages.WARNING
            )
            return
        screenplay = queryset.first()
        relative_path = screenplay.export_failed_checks_markdown()
        file_url = f"{settings.MEDIA_URL}{relative_path}"
        self.message_user(
            request,
            format_html(
                "Export complete! <a href='{}' target='_blank'>Download Markdown file</a>",
                file_url
            ),
            level=messages.SUCCESS
        )
        return HttpResponseRedirect(request.get_full_path())

    @admin.action(description="Check for Direct Camera Operations")
    def camera_operations_check(self, request, queryset):
        total = 0
        for sp in queryset:
            highlights = check_camera_operations(sp)
            total += len(highlights)
        self.message_user(
            request,
            ngettext(
                "%d camera operation found and highlighted.",
                "%d camera operations found and highlighted.",
                total,
            ) % total,
            messages.SUCCESS,
        )

    @admin.action(description="Check ‘Show, Don’t Tell’ Violations")
    def show_dont_tell_check_action(self, request, queryset):
        total = 0
        for sp in queryset:
            highlights = show_dont_tell_check(sp)
            total += len(highlights)
        self.message_user(
            request,
            ngettext(
                "%d narration-instead-of-showing instance flagged.",
                "%d narration-instead-of-showing instances flagged.",
                total,
            ) % total,
            messages.SUCCESS,
        )

    @admin.action(description="Identify Boring Scenes")
    def boring_scenes_check_action(self, request, queryset):
        total = 0
        for sp in queryset:
            highlights = boring_scenes_check(sp)
            total += len(highlights)
        self.message_user(
            request,
            ngettext(
                "%d potentially boring scene flagged.",
                "%d potentially boring scenes flagged.",
                total,
            ) % total,
            messages.SUCCESS,
        )

    @admin.action(description="Highlight Dead-End Scenes")
    def dead_end_check_action(self, request, queryset):
        total = 0
        for sp in queryset:
            highlights = dead_end_check(sp)
            total += len(highlights)
        self.message_user(
            request,
            ngettext(
                "%d dead-end scene highlighted.",
                "%d dead-end scenes highlighted.",
                total,
            ) % total,
            messages.SUCCESS,
        )


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = Character.Api.list

@admin.register(SceneHighlight)
class SceneHighlightAdmin(admin.ModelAdmin):
    list_display = SceneHighlight.Api.list

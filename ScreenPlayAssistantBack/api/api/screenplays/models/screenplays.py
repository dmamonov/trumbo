# Django
from django.db import models

# Models
from api.utils.models import BaseModel
from api.users.models import User
from pydantic import BaseModel as PydanticBaseModel, Field as PydanticField
from django.conf import settings
import os
from django.utils.text import slugify
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional
import re

class ScreenPlay(BaseModel):
    """
    Represents a screenplay document, including its title, content, and author.
    """
    title = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        help_text="The title of the screenplay."
    )
    content = RichTextUploadingField(
        null=True,
        blank=True,
        help_text="The full text content of the screenplay."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='screenplays',
        null=True,
        blank=True,
        help_text="The user who created or uploaded the screenplay."
    )

    class Meta:
        ordering = ['-created']
        verbose_name = "Screenplay"
        verbose_name_plural = "Screenplays"
        unique_together = ('title', 'created_by')

    def __str__(self):
        return self.title

    class Api:
        list = ['id', 'title', 'content', 'created_by']
        filter = ['created_by']
        search = ['id', 'title', 'content', 'created_by__name']
        write = ['id', 'title', 'content', 'created_by']
        
    @dataclass
    class ParsedScene:
        slugline: str
        content: str
        position: int


    def get_scenes(self, scene_markers: Optional[List[str]] = None) -> List[ParsedScene]:
        content = self.content
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
                    scenes.append(self.ParsedScene(
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
            scenes.append(self.ParsedScene(
                slugline=current_slug.strip() if current_slug else "UNKNOWN",
                content="\n".join(current_content).strip(),
                position=position
            ))

        return scenes

    
    def get_owner(self):
        return self.created_by

    def export_characters_markdown(screenplay):
        """
        Generate a Markdown string for characters in a screenplay and save it to a file.

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
                markdown += f"{character.names}\n"
                markdown += f"> _All names or nicknames mentioned in the story_\n\n"

                if character.role:
                    markdown += f"### Role in the Story\n{character.role}\n\n"

                if character.physical_appearance:
                    markdown += f"### Physical Appearance\n{character.physical_appearance}\n\n"

                if character.personal_qualities:
                    markdown += f"### Personal Qualities\n{character.personal_qualities}\n\n"

                if character.voice_style:
                    markdown += f"### Voice / Dialogue Style\n{character.voice_style}\n\n"

                if character.relationships:
                    markdown += f"### Relationships (with Other Characters)\n{character.relationships}\n\n"

                if character.internal_conflict or character.external_conflict:
                    markdown += f"### Conflicts\n"
                    if character.internal_conflict:
                        markdown += f"- **Internal Conflict**: {character.internal_conflict}\n"
                    if character.external_conflict:
                        markdown += f"- **External Conflict**: {character.external_conflict}\n"
                    markdown += "\n"

                if character.backstory:
                    markdown += f"### Backstory (Concise)\n{character.backstory}\n\n"

                if character.wants or character.stakes:
                    markdown += f"### Objective & Stakes\n"
                    if character.wants:
                        markdown += f"- **Wants**: {character.wants}\n"
                    if character.stakes:
                        markdown += f"- **Stakes**: {character.stakes}\n"
                    markdown += "\n"

                if character.character_arc:
                    markdown += f"### Character Arc\n{character.character_arc}\n\n"

                # Optional fallback content
                if not any([
                    character.role, character.physical_appearance, character.personal_qualities,
                    character.voice_style, character.relationships, character.internal_conflict,
                    character.external_conflict, character.backstory, character.wants,
                    character.stakes, character.character_arc
                ]):
                    if character.profile:
                        markdown += f"**Profile:**\n{character.profile}\n\n"
                    else:
                        markdown += "_No detailed information provided._\n\n"

                markdown += "---\n\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)

        return os.path.join('exports', filename)

    def export_failed_checks_markdown(screenplay) -> str:
        """
        Generate a Markdown report of all failed‐check highlights for this screenplay,
        save it to MEDIA_ROOT/exports/, and return the relative path to the file.
        """
        # Prepare output directory & filename
        output_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        slug = slugify(screenplay.title)
        filename = f"{slug}-failed-checks-{timestamp}.md"
        filepath = os.path.join(output_dir, filename)

        # Which checks to include
        check_types = [
            'camera_operation',
            'show_dont_tell',
            'boring_scene',
            'dead_end',
        ]

        # Fetch all highlights for these checks
        highlights = SceneHighlight.objects.filter(
            screenplay=screenplay,
            # name__in=check_types
        ).order_by('name', 'id')

        # Build Markdown
        md = [f"# Failed Checks for *{screenplay.title}*\n"]
        if not highlights:
            md.append("_No failed checks detected._\n")
        else:
            current = None
            for h in highlights:
                if h.name != current:
                    # New section
                    pretty = h.name.replace('_', ' ').title()
                    md.append(f"## {h.type}: {pretty}\n")
                    current = h.name

                # List each highlight
                snippet = h.related_text.replace('\n', ' ').strip()
                md.append(f"- **Text snippet:** `{snippet}`\n")
                md.append(f"  - **Issue:** {h.description.strip()}\n")

            md.append("")  # trailing newline

        # Write out the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(md))

        # Return the path relative to MEDIA_ROOT so you can do MEDIA_URL + relative_path
        return os.path.join('exports', filename)
    
    def export_conflict_points_markdown(screenplay) -> str:
        """
        Generate a Markdown report of all conflict points for this screenplay,
        save it to MEDIA_ROOT/exports/, and return the relative path to the file.
        """

        # Prepare output directory & filename
        output_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        slug = slugify(screenplay.title)
        filename = f"{slug}-conflict-points-{timestamp}.md"
        filepath = os.path.join(output_dir, filename)

        # Fetch conflict points
        conflict_points = ConflictPoint.objects.filter(screenplay=screenplay).order_by('start_scene_position')

        # Build Markdown
        md = [f"# Conflict Points for *{screenplay.title}*\n"]
        if not conflict_points:
            md.append("_No conflict points recorded._\n")
        else:
            for cp in conflict_points:
                md.append(cp.to_markdown())
                md.append("---")  # separator between conflicts

        # Write out the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(md))

        # Return the relative path for MEDIA_URL + relative_path usage
        return os.path.join('exports', filename)


class Character(BaseModel):
    """
    Represents a character in a screenplay.
    """
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        help_text="Full name of the character (e.g., 'Alice', 'Captain Nemo')."
    )
    names = models.CharField(
        max_length=128*4,
        null=True,
        blank=True,
        help_text="All names or nicknames mentioned in the story"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="A short description of the character's role or personality."
    )
    profile = models.TextField(
        null=True,
        blank=True,
        help_text="Detailed character profile including traits, backstory, etc."
    )
    role = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Role in the story (e.g., Protagonist, Antagonist, Supporting, etc.)"
    )
    physical_appearance = models.TextField(
        null=True,
        blank=True,
        help_text="Description of physical traits: age, build, style, distinguishing features, etc."
    )
    personal_qualities = models.TextField(
        null=True,
        blank=True,
        help_text="Core personality traits, strengths, flaws, quirks, habits, etc."
    )
    voice_style = models.TextField(
        null=True,
        blank=True,
        help_text="How the character speaks: Formal, sarcastic, poetic, blunt, etc."
    )
    relationships = models.TextField(
        null=True,
        blank=True,
        help_text="Relationships with other characters (name and short description)."
    )
    internal_conflict = models.TextField(
        null=True,
        blank=True,
        help_text="Emotional, moral, or psychological struggle."
    )
    external_conflict = models.TextField(
        null=True,
        blank=True,
        help_text="Conflict with people, systems, or environments."
    )
    backstory = models.TextField(
        null=True,
        blank=True,
        help_text="Key life events or background that shaped the character."
    )
    wants = models.TextField(
        null=True,
        blank=True,
        help_text="What the character actively wants to achieve."
    )
    stakes = models.TextField(
        null=True,
        blank=True,
        help_text="What they stand to gain or lose if they succeed or fail."
    )
    character_arc = models.TextField(
        null=True,
        blank=True,
        help_text="How the character changes—or resists change—through the story."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='characters',
        null=True,
        blank=True,
        help_text="The user who created or uploaded the character."
    )
    screenplay = models.ForeignKey(
        'ScreenPlay',
        on_delete=models.CASCADE,
        related_name='characters',
        null=True,
        blank=False,
        help_text="The screenplay this character belongs to."
    )

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'screenplay')  # Prevent duplicate characters per screenplay

    def __str__(self):
        return f"{self.name} ({self.screenplay.title if self.screenplay else 'No Screenplay'})"

    class Api:
        list = [
            'id', 'name', 'description', 'profile', 'role', 'physical_appearance',
            'personal_qualities', 'voice_style', 'relationships', 'internal_conflict',
            'external_conflict', 'backstory', 'wants', 'stakes', 'character_arc', 'created_by'
        ]
        filter = [
            'role', 'created_by', 'screenplay'
        ]
        search = [
            'name', 'description', 'profile', 'role', 'physical_appearance',
            'personal_qualities', 'voice_style', 'relationships', 'internal_conflict',
            'external_conflict', 'backstory', 'wants', 'stakes', 'character_arc'
        ]
        write = [
            'id', 'name', 'description', 'profile', 'role', 'physical_appearance',
            'personal_qualities', 'voice_style', 'relationships', 'internal_conflict',
            'external_conflict', 'backstory', 'wants', 'stakes', 'character_arc', 'created_by'
        ]

    class PydanticSchema(PydanticBaseModel):
        name: str
        names: str = PydanticField(
            ...,
            description="All names or nicknames mentioned in the story"
        )
        description: str
        profile: str = PydanticField(
            ...,
            description="The actions the character takes in the story and its whole arch in general"
        )
        role: str
        physical_appearance: str
        personal_qualities: str
        voice_style: str
        relationships: str
        internal_conflict: str
        external_conflict: str
        backstory: str
        wants: str
        stakes: str
        character_arc: str

    def get_owner(self):
        return self.created_by


class SceneHighlight(BaseModel):
    screenplay = models.ForeignKey(
        ScreenPlay,
        on_delete=models.CASCADE,
        related_name='highlights'
    )
    name = models.CharField(
        max_length=64,
        help_text="Which check flagged this highlight."
    )
    type = models.CharField(
        max_length=64,
        help_text="Type of Check",
        default=""
    )
    description = models.TextField(
        help_text="Why this scene was flagged."
    )
    related_text = models.TextField(
        help_text="The snippet of the screenplay this refers to."
    )
    criticality = models.CharField(
        max_length=32,
        help_text="How critical this highlight is (e.g., low, medium, high).",
        default="medium"
    )
    certainty = models.FloatField(
        help_text="How certain the system is about this highlight (0.0 to 1.0).",
        default=1.0
    )
    conclusion = models.TextField(
        help_text="What could be done improved",
        default=""
    )

    class Meta:
        ordering = ['screenplay', 'name']
    
    class Api:
        list = [
            'id', 'screenplay', 'name', 'description', 'related_text',
        ]
        filter = [
            'screenplay',
        ]
        search = [
            'name', 'description', 'related_text',
        ]
        write = [
            'id', 'screenplay', 'name', 'description', 'related_text',
        ]
    

    class PydanticSchema(PydanticBaseModel):
        name: str = PydanticField(..., description="Descriptive name of the error")
        description: str = PydanticField(..., description="Why this scene was flagged")
        related_text: str = PydanticField(..., description="The snippet of screenplay text that triggered the flag")
        criticality: str = PydanticField(..., description="How critical this highlight is")
        certainty: float = PydanticField(..., description="Certainty score from 0.0 to 1.0")
        conclusion: str = PydanticField(..., description="What could be done improved")


class ConflictPoint(BaseModel):
    screenplay = models.ForeignKey(
        ScreenPlay,
        on_delete=models.CASCADE,
        related_name='conflict_points'
    )
    conflict_name = models.TextField(
        help_text="Short title for the conflict."
    )
    introduced_at_regex = models.TextField(
        help_text="Where in the story the conflict is introduced (e.g., scene number, timestamp, or description)."
    )
    resolved_at_regex = models.TextField(
        help_text="Where in the story the conflict is resolved."
    )
    description = models.TextField(
        help_text="General description of the conflict."
    )
    criticality = models.CharField(
        max_length=32,
        help_text="How critical this conflict is to the story (e.g., low, medium, high).",
        default="medium"
    )
    certainty = models.FloatField(
        help_text="How certain the system is that this is a conflict (0.0 to 1.0).",
        default=1.0
    )
    conclusion = models.TextField(
        help_text="How the conflict contributes to the story or could be improved.",
        default=""
    )
    start_scene_position = models.IntegerField(
        help_text="Conflict scene start",
        default=0
    )
    last_updated_scene_position = models.IntegerField(
        help_text="Conflict scene end",
        default=0
    )

    class Meta:
        ordering = ['screenplay', ]

    class Api:
        list = [
            'id', 'screenplay', 'conflict_name', 'introduced_at_regex', 'resolved_at_regex',
            'description'
        ]
        filter = [
            'screenplay',
        ]
        search = [
            'conflict_name', 'description',
        ]
        write = [
            'id', 'screenplay', 'conflict_name', 'introduced_at_regex', 'resolved_at_regex',
            'description',
        ]

    class PydanticSchema(PydanticBaseModel):
        conflict_name: str = PydanticField(..., description="Short title for the conflict")
        criticality: str = PydanticField(..., description="Importance of the conflict")
        certainty: float = PydanticField(..., description="Certainty that this is a conflict")
        conclusion: str = PydanticField(..., description="How the conflict plays out or can be improved")
        description: str = PydanticField(..., description="General description of the conflict")
        introduced_at_regex: str = PydanticField(..., description="regex pattern to find Screenplay snippet where conflict is shown")
        resolved_at_regex: str = PydanticField(..., description="regex pattern to find Screenplay snippet where conflict is resolved")

    def to_markdown(self):
        """
        Returns a Markdown-formatted string with conflict details.
        """
        return f"""### 🧨 Conflict: {self.conflict_name}

**🟡 Criticality:** {self.criticality}  
**🔍 Certainty:** {self.certainty:.2f}  
**🎬 Introduced At:** `{self.introduced_at_regex}`  
**✅ Resolved At:** `{self.resolved_at_regex}`  
**📝 Description:**  
{self.description.strip()}

**🧠 Conclusion:**  
{self.conclusion.strip() if self.conclusion else "_No conclusion provided._"}

**📍 Scene Range:** {self.start_scene_position} → {self.last_updated_scene_position}
"""
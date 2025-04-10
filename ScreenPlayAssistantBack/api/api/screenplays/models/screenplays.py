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
from django.conf import settings

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
    content = models.TextField(
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

    class PydanticSchema(PydanticBaseModel):
        name: str
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

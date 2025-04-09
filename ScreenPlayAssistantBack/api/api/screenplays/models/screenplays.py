# Django
from django.db import models

# Models
from api.utils.models import BaseModel
from api.users.models import User
from pydantic import BaseModel as PydanticBaseModel, Field as PydanticField
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
        list = ['id', 'name', 'description', 'profile', 'created_by']
    
    class PydanticSchema(PydanticBaseModel):
        name: str
        description: str
        profile: str = PydanticField(
            ...,
            description="The actions the character takes in the story and its whole arch in general"
        )
    
    def get_owner(self):
        return self.created_by
    
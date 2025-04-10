# Generated by Django 3.2 on 2025-04-10 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screenplays', '0002_auto_20250406_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='backstory',
            field=models.TextField(blank=True, help_text='Key life events or background that shaped the character.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='character_arc',
            field=models.TextField(blank=True, help_text='How the character changes—or resists change—through the story.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='external_conflict',
            field=models.TextField(blank=True, help_text='Conflict with people, systems, or environments.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='internal_conflict',
            field=models.TextField(blank=True, help_text='Emotional, moral, or psychological struggle.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='personal_qualities',
            field=models.TextField(blank=True, help_text='Core personality traits, strengths, flaws, quirks, habits, etc.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='physical_appearance',
            field=models.TextField(blank=True, help_text='Description of physical traits: age, build, style, distinguishing features, etc.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='relationships',
            field=models.TextField(blank=True, help_text='Relationships with other characters (name and short description).', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='role',
            field=models.CharField(blank=True, help_text='Role in the story (e.g., Protagonist, Antagonist, Supporting, etc.)', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='stakes',
            field=models.TextField(blank=True, help_text='What they stand to gain or lose if they succeed or fail.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='voice_style',
            field=models.TextField(blank=True, help_text='How the character speaks: Formal, sarcastic, poetic, blunt, etc.', null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='wants',
            field=models.TextField(blank=True, help_text='What the character actively wants to achieve.', null=True),
        ),
    ]

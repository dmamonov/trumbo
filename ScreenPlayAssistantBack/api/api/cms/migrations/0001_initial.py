# Generated by Django 3.2 on 2023-02-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('content_text', models.TextField(blank=True, null=True)),
                ('content_text_es', models.TextField(blank=True, null=True)),
                ('content_text_en', models.TextField(blank=True, null=True)),
                ('content_image', models.ImageField(blank=True, null=True, upload_to='content/%Y/%m/%d/')),
                ('content_number', models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True)),
                ('content_json', models.JSONField(blank=True, null=True)),
                ('content_type', models.CharField(choices=[('T', 'Text'), ('N', 'Number'), ('I', 'Image'), ('J', 'Json')], default='T', max_length=5)),
            ],
        ),
    ]

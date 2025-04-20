# Django REST Framework
from rest_framework import serializers

# Models
from api.screenplays.models import *

class ScreenPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenPlay
        fields = ScreenPlay.Api.list


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = Character.Api.list

class SceneHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneHighlight
        fields = SceneHighlight.Api.list
    

class WriteScreenPlaySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ScreenPlay
        fields = ScreenPlay.Api.write


class WriteCharacterSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Character
        fields = Character.Api.write

class WriteSceneHighlightSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SceneHighlight
        fields = SceneHighlight.Api.write
    
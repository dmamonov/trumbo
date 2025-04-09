# User serializers

# Rest Framework
from rest_framework import serializers

# Models
from api.cms.models import Content, ContentType

# Utilities
from django.conf import settings

def validate_language(value):
    if value in [x[0] for x in settings.LANGUAGES]:
        return True
    return False


class ContentSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(choices=ContentType.choices)

    class Meta:
        model = Content
        fields = [ 
            'name', 'content', 'content_type'
        ]
    
    def to_representation(self, instance):
        # get language from request
        language = self.context['request'].query_params.get('language')
        if not language:
            language = 'en'
        elif not validate_language(language):
            raise serializers.ValidationError('Language not supported')
        
        repr = super().to_representation(instance)
        repr['content'] = instance.get_traduction(language)
        return repr

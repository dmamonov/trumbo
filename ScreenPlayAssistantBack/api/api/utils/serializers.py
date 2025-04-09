from rest_framework import serializers

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return str(self._choices[obj])

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val.lower() == data.lower():
                return key
        self.fail('invalid_choice', input=data)
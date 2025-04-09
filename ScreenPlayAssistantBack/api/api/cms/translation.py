from modeltranslation.translator import translator, TranslationOptions
from api.cms.models import Content

class ContentTranslationOptions(TranslationOptions):
    fields = ('content_text',)

translator.register(Content, ContentTranslationOptions)

# Django
from django.urls import include, path, re_path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from api.screenplays.views import *

router = DefaultRouter()

router.register(r'screen-plays', ScreenPlaysViewSet, basename='screen_plays')
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'scene-highlight', SceneHighlightViewSet, basename='scene_highlight')

urlpatterns = [
    path('', include(router.urls)),
]

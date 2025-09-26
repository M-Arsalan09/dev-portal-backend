from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DeveloperViewSet, SkillAreaViewSet, DeveloperProjectsViewSet

router = DefaultRouter()

router.register(r'developers', DeveloperViewSet, basename='developer')
router.register(r'skill-areas', SkillAreaViewSet, basename='skill-area')
router.register(r'developer-projects', DeveloperProjectsViewSet, basename='developer-project')


urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from . import views

app_name = 'agent'

urlpatterns = [
    path('query/', views.query_gemini, name='query_gemini'),
    path('analyze-project/', views.analyze_project, name='analyze_project'),
]

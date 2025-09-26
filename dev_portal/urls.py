from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("developers.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/agent/", include("agent.urls")),
]

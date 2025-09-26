from django.contrib import admin
from .models import Developers, SkillAreas, Skills, DeveloperSkills, DeveloperProjects, DeveloperSkillLevel

# Register your models here.

@admin.register(Developers)
class DevelopersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'role', 'industry_experience', 'is_available']
    list_filter = ['role', 'is_available']
    search_fields = ['name', 'email']

@admin.register(SkillAreas)
class SkillAreasAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill_area', 'created_at']
    list_filter = ['skill_area']

@admin.register(DeveloperSkills)
class DeveloperSkillsAdmin(admin.ModelAdmin):
    list_display = ['developer', 'skill', 'created_at']
    list_filter = ['skill__skill_area']

@admin.register(DeveloperProjects)
class DeveloperProjectsAdmin(admin.ModelAdmin):
    list_display = ['developer', 'name', 'project_origin', 'created_at']
    list_filter = ['project_origin', 'created_at']
    filter_horizontal = ['project_categories', 'skills']

@admin.register(DeveloperSkillLevel)
class DeveloperSkillLevelAdmin(admin.ModelAdmin):
    list_display = ['developer', 'skill', 'level', 'project_count', 'last_updated']
    list_filter = ['level', 'skill__skill_area']
    readonly_fields = ['project_count', 'last_updated', 'created_at']

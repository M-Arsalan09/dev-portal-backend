from rest_framework import serializers
from .models import ProjectCategory, ProjectCategorySkills


class ProjectCategorySerializer(serializers.ModelSerializer):
    use_cases = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        required=False
    )
    
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'description', 'use_cases']
        
class ProjectCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'description']

class ProjectCategorySkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategorySkills
        fields = ['id', 'project_category', 'skill']
from rest_framework import serializers

from .models import Developers, SkillAreas, DeveloperProjects, DeveloperSkillLevel
from .services import SkillLevelService


class DeveloperListSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=200)
    role = serializers.CharField(max_length=100)
    industry_experience = serializers.IntegerField()
    is_available = serializers.BooleanField()
    overall_level = serializers.SerializerMethodField()
    
    def get_overall_level(self, obj):
        """Get the overall developer level based on skill levels."""
        return SkillLevelService.get_developer_overall_level(obj)
    

class DeveloperSerializer(serializers.ModelSerializer):
    overall_level = serializers.SerializerMethodField()
    
    class Meta:
        model = Developers
        fields = ['name', 'email', 'role', 'graduation_date', 'industry_experience', 'employment_start_date', 'is_available', 'overall_level']
        extra_kwargs = {
            'skills': {'read_only': True}
        }
    
    def get_overall_level(self, obj):
        """Get the overall developer level based on skill levels."""
        return SkillLevelService.get_developer_overall_level(obj)
        
        
class SkillAreaSerializer(serializers.ModelSerializer):
    skills_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SkillAreas
        fields = '__all__'
        
    def get_skills_count(self, obj):
        from .models import Skills
        skills = Skills.objects.filter(skill_area=obj)
        return skills.count()

        
class DeveloperProjectsListSerializer(serializers.ModelSerializer):
    developer_name = serializers.CharField(source='developer.name')
    
    class Meta:
        model = DeveloperProjects
        fields = ['id', 'developer_name', 'name', 'description', 'tech_stack', 'project_origin']
        
class DeveloperProjectsSerializer(serializers.ModelSerializer):
    developer_name = serializers.CharField(source='developer.name', read_only=True)
    
    class Meta:
        model = DeveloperProjects
        fields = ['id', 'name', 'description', 'tech_stack', 'project_origin', 'repo_link', 'doc_link', 'presentation_link', 'live_link', 'created_at', 'developer', 'developer_name', 'project_categories', 'skills']

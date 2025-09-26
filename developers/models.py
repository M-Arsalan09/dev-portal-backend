from django.db import models
from projects.models import ProjectCategory

# Create your models here.
class Developers(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)
    
    graduation_date = models.DateField()
    industry_experience = models.IntegerField()
    employment_start_date = models.DateField()
    
    is_available = models.BooleanField(default=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.role})"
    

class SkillAreas(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Skills(models.Model):
    name = models.CharField(max_length=200)
    skill_area = models.ForeignKey(SkillAreas, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class DeveloperSkills(models.Model):
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.developer.name} - {self.skill.name}"
    
    
class DeveloperProjects(models.Model):
    
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE, related_name='developer_projects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # one project can have multiple project categories
    project_categories = models.ManyToManyField(ProjectCategory, related_name='developer_projects')
    tech_stack = models.JSONField(default=list)
    project_origin = models.CharField(max_length=200)
    # one project can have multiple skills from the skills table
    skills = models.ManyToManyField(Skills, related_name='developer_projects')
    
    repo_link = models.URLField(blank=True, null=True)
    doc_link = models.URLField(blank=True, null=True)
    presentation_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.developer.name} - {self.name}"


class DeveloperSkillLevel(models.Model):
    """
    Model to track skill levels for developers based on their projects.
    Level 0: Basic knowledge (no projects)
    Level 1: Beginner (1 project)
    Level 2: Advanced (3 projects)
    Level 3: Expert (5+ projects)
    """
    LEVEL_CHOICES = [
        (0, 'Basic Knowledge'),
        (1, 'Beginner'),
        (2, 'Advanced'),
        (3, 'Expert'),
    ]
    
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE, related_name='skill_levels')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='developer_levels')
    level = models.IntegerField(choices=LEVEL_CHOICES, default=0)
    project_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['developer', 'skill']
    
    def __str__(self):
        return f"{self.developer.name} - {self.skill.name} (Level {self.level})"
    
    
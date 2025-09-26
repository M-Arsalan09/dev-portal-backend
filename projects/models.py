from django.db import models
# from developers.models import Skills


class ProjectCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    use_cases = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class ProjectCategorySkills(models.Model):
    # from developers.models import Skills
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    skill = models.ForeignKey('developers.Skills', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project_category.name} - {self.skill.name}"

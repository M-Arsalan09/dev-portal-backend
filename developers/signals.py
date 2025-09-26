from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import DeveloperProjects, DeveloperSkills
from .services import SkillLevelService


@receiver(post_save, sender=DeveloperProjects)
def update_skill_levels_on_project_save(sender, instance, created, **kwargs):
    """
    Update skill levels when a developer project is saved.
    """
    SkillLevelService.update_developer_skill_levels(instance.developer)


@receiver(post_delete, sender=DeveloperProjects)
def update_skill_levels_on_project_delete(sender, instance, **kwargs):
    """
    Update skill levels when a developer project is deleted.
    """
    SkillLevelService.update_developer_skill_levels(instance.developer)


@receiver(m2m_changed, sender=DeveloperProjects.skills.through)
def update_skill_levels_on_project_skills_change(sender, instance, action, pk_set, **kwargs):
    """
    Update skill levels when skills are added or removed from a project.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        SkillLevelService.update_developer_skill_levels(instance.developer)


@receiver(post_save, sender=DeveloperSkills)
def update_skill_levels_on_skill_add(sender, instance, created, **kwargs):
    """
    Update skill levels when a developer skill is added.
    """
    if created:
        SkillLevelService.update_developer_skill_levels(instance.developer)


@receiver(post_delete, sender=DeveloperSkills)
def update_skill_levels_on_skill_remove(sender, instance, **kwargs):
    """
    Update skill levels when a developer skill is removed.
    """
    SkillLevelService.update_developer_skill_levels(instance.developer)

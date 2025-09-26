from django.db import transaction
from .models import Developers, DeveloperSkills, DeveloperProjects, DeveloperSkillLevel, Skills


class SkillLevelService:
    """
    Service class to handle skill level calculations and updates for developers.
    """
    
    @staticmethod
    def calculate_skill_level(project_count):
        """
        Calculate skill level based on project count.
        
        Args:
            project_count (int): Number of projects for a specific skill
            
        Returns:
            int: Skill level (0-3)
        """
        if project_count == 0:
            return 0  # Basic Knowledge
        elif project_count == 1:
            return 1  # Beginner
        elif project_count <= 3:
            return 2  # Advanced
        else:
            return 3  # Expert
    
    @staticmethod
    def get_skill_level_name(level):
        """
        Get the human-readable name for a skill level.
        
        Args:
            level (int): Skill level (0-3)
            
        Returns:
            str: Level name
        """
        level_names = {
            0: 'Basic Knowledge',
            1: 'Beginner',
            2: 'Advanced',
            3: 'Expert'
        }
        return level_names.get(level, 'Unknown')
    
    @staticmethod
    def update_developer_skill_levels(developer):
        """
        Update skill levels for a specific developer based on their projects.
        
        Args:
            developer (Developers): Developer instance
        """
        # Get all skills that the developer has claimed
        developer_skills = DeveloperSkills.objects.filter(developer=developer)
        
        for dev_skill in developer_skills:
            skill = dev_skill.skill
            
            # Count projects that use this skill
            project_count = DeveloperProjects.objects.filter(
                developer=developer,
                skills=skill
            ).count()
            
            # Calculate the new level
            new_level = SkillLevelService.calculate_skill_level(project_count)
            
            # Update or create the skill level record
            skill_level, created = DeveloperSkillLevel.objects.update_or_create(
                developer=developer,
                skill=skill,
                defaults={
                    'level': new_level,
                    'project_count': project_count
                }
            )
    
    @staticmethod
    def update_all_developers_skill_levels():
        """
        Update skill levels for all developers.
        """
        developers = Developers.objects.all()
        for developer in developers:
            SkillLevelService.update_developer_skill_levels(developer)
    
    @staticmethod
    def get_developer_overall_level(developer):
        """
        Determine the overall developer level based on their skill levels.
        
        Args:
            developer (Developers): Developer instance
            
        Returns:
            dict: Overall level information
        """
        skill_levels = DeveloperSkillLevel.objects.filter(developer=developer)
        
        if not skill_levels.exists():
            return {
                'level': 0,
                'level_name': 'Basic Knowledge',
                'description': 'No skill levels available'
            }
        
        # Count skills by level
        level_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        for skill_level in skill_levels:
            level_counts[skill_level.level] += 1
        
        total_skills = len(skill_levels)
        
        # Determine overall level based on majority
        if level_counts[3] > level_counts[2] and level_counts[3] > level_counts[1] and level_counts[3] > level_counts[0]:
            overall_level = 3
            level_name = 'Expert'
            description = f'Expert in {level_counts[3]} out of {total_skills} skills'
        elif level_counts[2] > level_counts[1] and level_counts[2] > level_counts[0]:
            overall_level = 2
            level_name = 'Advanced'
            description = f'Advanced in {level_counts[2]} out of {total_skills} skills'
        elif level_counts[1] > level_counts[0]:
            overall_level = 1
            level_name = 'Beginner'
            description = f'Beginner in {level_counts[1]} out of {total_skills} skills'
        else:
            overall_level = 0
            level_name = 'Basic Knowledge'
            description = f'Basic knowledge in {level_counts[0]} out of {total_skills} skills'
        
        return {
            'level': overall_level,
            'level_name': level_name,
            'description': description,
            'skill_breakdown': {
                'expert': level_counts[3],
                'advanced': level_counts[2],
                'beginner': level_counts[1],
                'basic_knowledge': level_counts[0],
                'total_skills': total_skills
            }
        }
    
    @staticmethod
    def get_developer_skill_levels_with_details(developer):
        """
        Get detailed skill level information for a developer.
        
        Args:
            developer (Developers): Developer instance
            
        Returns:
            list: List of skill level details grouped by skill area
        """
        skill_levels = DeveloperSkillLevel.objects.filter(developer=developer).select_related('skill', 'skill__skill_area')
        
        # Group by skill area
        skill_areas_dict = {}
        for skill_level in skill_levels:
            skill_area_id = skill_level.skill.skill_area.id
            skill_area_name = skill_level.skill.skill_area.name
            
            if skill_area_id not in skill_areas_dict:
                skill_areas_dict[skill_area_id] = {
                    "skill_area_id": skill_area_id,
                    "skill_area_name": skill_area_name,
                    "skills": []
                }
            
            skill_areas_dict[skill_area_id]["skills"].append({
                "skill_id": skill_level.skill.id,
                "skill_name": skill_level.skill.name,
                "level": skill_level.level,
                "level_name": SkillLevelService.get_skill_level_name(skill_level.level),
                "project_count": skill_level.project_count,
                "last_updated": skill_level.last_updated
            })
        
        return list(skill_areas_dict.values())

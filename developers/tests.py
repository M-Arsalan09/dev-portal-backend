from django.test import TestCase
from django.contrib.auth.models import User
from .models import Developers, SkillAreas, Skills, DeveloperSkills, DeveloperProjects, DeveloperSkillLevel
from .services import SkillLevelService


class SkillLevelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.skill_area = SkillAreas.objects.create(name="Programming")
        self.skill1 = Skills.objects.create(name="Python", skill_area=self.skill_area)
        self.skill2 = Skills.objects.create(name="JavaScript", skill_area=self.skill_area)
        
        self.developer = Developers.objects.create(
            name="Test Developer",
            email="test@example.com",
            role="Developer",
            graduation_date="2020-01-01",
            industry_experience=2,
            employment_start_date="2020-01-01"
        )
        
        # Add skills to developer
        DeveloperSkills.objects.create(developer=self.developer, skill=self.skill1)
        DeveloperSkills.objects.create(developer=self.developer, skill=self.skill2)
    
    def test_skill_level_calculation(self):
        """Test skill level calculation based on project count."""
        # Test level 0 (no projects)
        level = SkillLevelService.calculate_skill_level(0)
        self.assertEqual(level, 0)
        
        # Test level 1 (1 project)
        level = SkillLevelService.calculate_skill_level(1)
        self.assertEqual(level, 1)
        
        # Test level 2 (3 projects)
        level = SkillLevelService.calculate_skill_level(3)
        self.assertEqual(level, 2)
        
        # Test level 3 (5+ projects)
        level = SkillLevelService.calculate_skill_level(5)
        self.assertEqual(level, 3)
    
    def test_skill_level_update(self):
        """Test updating skill levels for a developer."""
        # Initially should have level 0 for both skills
        SkillLevelService.update_developer_skill_levels(self.developer)
        
        skill_level1 = DeveloperSkillLevel.objects.get(developer=self.developer, skill=self.skill1)
        self.assertEqual(skill_level1.level, 0)
        self.assertEqual(skill_level1.project_count, 0)
        
        # Add a project with skill1
        project = DeveloperProjects.objects.create(
            developer=self.developer,
            name="Test Project",
            project_origin="Personal"
        )
        project.skills.add(self.skill1)
        
        # Update skill levels
        SkillLevelService.update_developer_skill_levels(self.developer)
        
        skill_level1.refresh_from_db()
        self.assertEqual(skill_level1.level, 1)
        self.assertEqual(skill_level1.project_count, 1)
    
    def test_overall_developer_level(self):
        """Test overall developer level calculation."""
        # Create skill levels
        DeveloperSkillLevel.objects.create(
            developer=self.developer,
            skill=self.skill1,
            level=1,
            project_count=1
        )
        DeveloperSkillLevel.objects.create(
            developer=self.developer,
            skill=self.skill2,
            level=2,
            project_count=3
        )
        
        overall_level = SkillLevelService.get_developer_overall_level(self.developer)
        
        self.assertEqual(overall_level['level'], 2)  # Advanced (majority)
        self.assertEqual(overall_level['level_name'], 'Advanced')

from django.core.management.base import BaseCommand
from developers.services import SkillLevelService


class Command(BaseCommand):
    help = 'Initialize skill levels for all developers based on their existing projects'

    def handle(self, *args, **options):
        self.stdout.write('Starting skill level initialization...')
        
        try:
            SkillLevelService.update_all_developers_skill_levels()
            self.stdout.write(
                self.style.SUCCESS('Successfully initialized skill levels for all developers')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error initializing skill levels: {str(e)}')
            )

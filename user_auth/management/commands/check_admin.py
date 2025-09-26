from django.core.management.base import BaseCommand
from user_auth.models import UserAuth


class Command(BaseCommand):
    help = 'Check if admin user exists and create if needed'

    def handle(self, *args, **options):
        admin_user = UserAuth.objects.filter(email="admin@gmail.com").first()
        
        if admin_user:
            self.stdout.write(
                self.style.SUCCESS('Admin user exists: admin@gmail.com')
            )
            self.stdout.write(f'Role: {admin_user.role}')
            self.stdout.write(f'First login: {admin_user.first_login}')
        else:
            self.stdout.write(
                self.style.ERROR('Admin user does not exist: admin@gmail.com')
            )

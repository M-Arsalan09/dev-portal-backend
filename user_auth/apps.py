from django.apps import AppConfig
from django.contrib.auth.hashers import make_password


class UserAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_auth"
    
    def ready(self):
        """
        Create admin user if it doesn't exist when the app starts.
        """
        try:
            from .models import UserAuth
            
            # Check if admin user exists
            admin_user = UserAuth.objects.filter(email="admin@gmail.com").first()
            
            if not admin_user:
                # Create admin user
                UserAuth.objects.create(
                    email="admin@gmail.com",
                    password=make_password("Admin123"),
                    role="admin",
                    first_login=False
                )
                print("Admin user created successfully: admin@gmail.com")
            else:
                print("Admin user already exists: admin@gmail.com")
                
        except Exception as e:
            # Handle case where database might not be ready yet
            print(f"Could not create admin user: {e}")

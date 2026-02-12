from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Recreates a superuser named "admin".'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'
        
        try:
            # Delete if exists to ensure clean state
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"User '{username}' found. Deleting to recreate...")
                User.objects.get(username=username).delete()
            
            # Create fresh
            self.stdout.write(f"Creating superuser '{username}'...")
            User.objects.create_superuser(
                username=username, 
                email=email, 
                password=password,
                dni='00000000', 
                full_name='Administrator'
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully with password '{password}'."))
            
            # Verify
            count = User.objects.count()
            self.stdout.write(f"Total users in DB: {count}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in init_admin: {e}"))

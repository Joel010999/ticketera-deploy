import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketera_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from events.models import Event, TicketType

User = get_user_model()

def setup():
    # 1. Create Superuser
    # 1. Ensure Superuser
    try:
        if not User.objects.filter(username='admin').exists():
            print("Creating superuser 'admin'...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin', dni='00000000', full_name='Administrator')
        else:
            print("Superuser 'admin' already exists. Updating password...")
            u = User.objects.get(username='admin')
            u.set_password('admin')
            u.save()
            print("Password for 'admin' updated to 'admin'.")
    except Exception as e:
        print(f"Error creating/updating superuser: {e}")

    # 2. Create Sample Event
    if not Event.objects.exists():
        print("Creating sample event...")
        event = Event.objects.create(
            title="Gran Concierto de Rock",
            description="El mejor evento del año. Bandas en vivo, comida y bebida. No te lo pierdas.",
            date=timezone.now() + timedelta(days=30),
            venue="Estadio Monumental",
        )
        
        # 3. Create Ticket Types
        TicketType.objects.create(event=event, name="General", price=5000.00, stock=100)
        TicketType.objects.create(event=event, name="VIP", price=12000.00, stock=20)
        TicketType.objects.create(event=event, name="Super VIP", price=25000.00, stock=5)
        
        print("Sample event 'Gran Concierto de Rock' created with tickets.")
    else:
        print("Events already exist. Skipping creation.")

if __name__ == '__main__':
    setup()

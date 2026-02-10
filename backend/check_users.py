import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all()

if users.exists():
    print("Existing users found:")
    for user in users:
        print(f"- Username: {user.username} (Superuser: {user.is_superuser})")
    print("\nPlease use one of these accounts. If you don't know the password, I can reset it for 'admin'.")
else:
    print("No users found. Creating default superuser...")
    try:
        User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        print("Superuser created successfully!")
        print("Username: admin")
        print("Password: password123")
    except Exception as e:
        print(f"Error creating superuser: {e}")

from django.core.management.base import BaseCommand

import json
import os

from authuser.models import User

#python manage.py export_users
#python manage.py changepassword gen@mail.ru

class Command(BaseCommand):
    help = 'Export user data (excluding passwords) to JSON'

    def handle(self, *args, **options):
        users = User.objects.all().values('id', 'email', 'name', 'is_staff', 'is_superuser', 'is_active')
        user_data = list(users)

        #Создадим директорию, если её нет
        os.makedirs('exports', exist_ok=True)
        filepath = os.path.join('exports', 'users.json')

        with open(filepath, 'w') as f:
            json.dump(user_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f'User data exported to {filepath}'))
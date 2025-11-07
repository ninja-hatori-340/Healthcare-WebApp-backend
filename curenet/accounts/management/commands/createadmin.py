from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Creates a superuser/admin account with ADMIN role'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for admin')
        parser.add_argument('--email', type=str, help='Email for admin')
        parser.add_argument('--password', type=str, help='Password for admin')
        parser.add_argument('--noinput', action='store_true', help='Use provided arguments without prompts')

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        noinput = options.get('noinput')

        if not noinput:
            if not username:
                username = input('Username: ')
            if not email:
                email = input('Email: ')
            if not password:
                password = input('Password: ')

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Username, email, and password are required.'))
            return

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User with username "{username}" already exists.'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'User with email "{email}" already exists.'))
            return

        # Create admin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'Role: {user.get_role_display()}'))
        self.stdout.write(self.style.SUCCESS('You can now login at /admin/ or /accounts/login/'))


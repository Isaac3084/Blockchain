import subprocess
import sys
import os
import django
from django.core.management import execute_from_command_line

def create_project_structure():
    """Create Django project structure"""
    try:
        # Create main project directory
        if not os.path.exists('Notary'):
            subprocess.run([sys.executable, '-m', 'django-admin', 'startproject', 'Notary', '.'])
            print("✓ Created Django project")
        
        # Create NotaryApp
        if not os.path.exists('NotaryApp'):
            subprocess.run([sys.executable, 'manage.py', 'startapp', 'NotaryApp'])
            print("✓ Created NotaryApp")
        
        # Create directories
        dirs = [
            'NotaryApp/templates/NotaryApp',
            'NotaryApp/static/css',
            'NotaryApp/static/js',
            'NotaryApp/static/images',
            'NotaryApp/utils',
            'media'
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        
        print("✓ Created project directories")
        return True
    except Exception as e:
        print(f"❌ Error creating project structure: {str(e)}")
        return False

def setup_database():
    """Setup database and run migrations"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notary.settings')
        django.setup()
        
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("✓ Created admin user")
        
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def setup_project():
    """Main setup function"""
    print("\n=== Starting Notarization System Setup ===\n")
    
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    
    if not create_project_structure():
        return False
    
    if not setup_database():
        return False
    
    print("\n✓ Setup completed successfully!")
    print("\nTo start the development server:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/")
    print("\nDefault admin credentials:")
    print("Username: admin")
    print("Password: admin")
    
    return True

if __name__ == "__main__":
    setup_project() 
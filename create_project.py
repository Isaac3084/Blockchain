import os
import subprocess
import sys

def create_project_structure():
    """Create the basic Django project structure"""
    
    # Create main project directory if it doesn't exist
    if not os.path.exists('Notary'):
        subprocess.run([sys.executable, '-m', 'django-admin', 'startproject', 'Notary', '.'])
        print("✓ Created Django project 'Notary'")
    
    # Create the NotaryApp if it doesn't exist
    if not os.path.exists('NotaryApp'):
        subprocess.run([sys.executable, 'manage.py', 'startapp', 'NotaryApp'])
        print("✓ Created Django app 'NotaryApp'")
    
    # Create templates directory structure
    templates_dir = os.path.join('NotaryApp', 'templates', 'NotaryApp')
    os.makedirs(templates_dir, exist_ok=True)
    print("✓ Created templates directory")

if __name__ == "__main__":
    create_project_structure() 
#!/usr/bin/env python
import os
import sys
import subprocess
import webbrowser
from time import sleep
import setup_contract  # Add this line with other imports

def print_banner():
    """Print welcome banner"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║     Blockchain-Based Autonomous Notarization System            ║
║                Using National eID Card                         ║
╚════════════════════════════════════════════════════════════════╝
    """)

def create_directories():
    """Create necessary directories"""
    dirs = ['static', 'media', 'templates']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✓ Created project directories")

def setup_django_project():
    """Setup Django project structure"""
    try:
        # Create project structure
        from create_project import create_project_structure
        create_project_structure()
        
        # Create necessary directories
        create_directories()
        
        return True
    except Exception as e:
        print(f"❌ Error setting up Django project: {str(e)}")
        return False

def check_environment():
    """Check if all required environment variables and files are present"""
    required_files = [
        'manage.py',
        'requirements.txt',
        '.env',
        'Notary.json'
    ]
    
    required_env_vars = [
        'INFURA_PROJECT_ID',
        'INFURA_PROJECT_SECRET',
        'ETH_ACCOUNT_ADDRESS',
        'ETH_PRIVATE_KEY'
    ]
    
    # Check files
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("❌ Missing required files:")
        for f in missing_files:
            print(f"   - {f}")
        return False
        
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
        
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    try:
        if not os.path.exists('venv'):
            print("Creating virtual environment...")
            subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
        
        # Activate virtual environment
        if sys.platform == 'win32':
            activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
            os.system(f'call {activate_script}')
        else:
            activate_script = os.path.join('venv', 'bin', 'activate')
            os.system(f'source {activate_script}')
            
        print("✅ Virtual environment setup complete")
        return True
    except Exception as e:
        print(f"❌ Error setting up virtual environment: {str(e)}")
        return False

def install_requirements():
    """Install required packages"""
    try:
        print("\nInstalling required packages...")
        # First upgrade pip
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install packages one by one
        with open('requirements.txt') as f:
            packages = f.read().splitlines()
        
        for package in packages:
            if package and not package.startswith('#'):
                try:
                    print(f"Installing {package}...")
                    subprocess.check_call([
                        sys.executable, 
                        '-m', 
                        'pip', 
                        'install', 
                        package,
                        '--no-cache-dir'  # Added to avoid caching issues
                    ])
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Failed to install {package}: {str(e)}")
                    continue
        
        print("✓ Required packages installed")
        return True
        
    except Exception as e:
        print(f"❌ Error installing requirements: {str(e)}")
        return False

def run_setup():
    """Run the setup script"""
    try:
        print("\nRunning project setup...")
        
        # Install requirements first
        if not install_requirements():
            return False
        
        # Then set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notary.settings')
        import django
        django.setup()
        
        # Run migrations
        print("\nRunning database migrations...")
        try:
            from django.core.management import execute_from_command_line
            # Remove existing migrations
            import shutil
            migrations_dir = 'NotaryApp/migrations'
            if os.path.exists(migrations_dir):
                for f in os.listdir(migrations_dir):
                    if f != '__init__.py' and os.path.isfile(os.path.join(migrations_dir, f)):
                        os.remove(os.path.join(migrations_dir, f))
            
            # Remove existing database
            if os.path.exists('db.sqlite3'):
                os.remove('db.sqlite3')
                
            # Create new migrations
            execute_from_command_line(['manage.py', 'makemigrations', 'NotaryApp'])
            execute_from_command_line(['manage.py', 'migrate'])
            
            # Create superuser
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin')
                print("✓ Created admin user")
                
            print("✓ Database migrations complete")
        except Exception as e:
            print(f"❌ Error running migrations: {str(e)}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Error running setup: {str(e)}")
        return False

def start_server():
    """Start the Django development server"""
    try:
        # Set the Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notary.settings')
        
        # Start the server
        print("\n🚀 Starting development server...")
        server_process = subprocess.Popen([sys.executable, 'manage.py', 'runserver'])
        
        # Wait a moment for the server to start
        sleep(2)
        
        # Open the browser
        webbrowser.open('http://127.0.0.1:8000/')
        
        print("""
✅ Server is running!
   - URL: http://127.0.0.1:8000/
   - Press Ctrl+C to stop the server

👤 Default admin credentials:
   - Username: admin
   - Password: admin
        """)
        
        # Keep the server running
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping server...")
        server_process.terminate()
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        return False

def main():
    """Main function to run the project"""
    print_banner()
    
    # Setup Django project structure
    if not setup_django_project():
        print("\n❌ Django project setup failed.")
        return
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above and try again.")
        return
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("\n❌ Virtual environment setup failed.")
        return
        
    # Install requirements and run setup
    if not run_setup():
        print("\n❌ Project setup failed.")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 
from django.core.management import execute_from_command_line

def run_migrations():
    """Run Django migrations"""
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        return True
    except Exception as e:
        print(f"❌ Error running migrations: {str(e)}")
        return False 
import json
import os
from web3 import Web3
from eth_account import Account
import eth_utils
import django
from django.conf import settings
from migration_manager import run_migrations

class DummyContract:
    def __init__(self):
        self.notary_count = 0
        self.user_count = 0
        self.notary_list = {}
        self.user_list = {}
        
    def register_hash(self, username, filename, hash_code, signature, date, key):
        """Dummy function to simulate contract hash registration"""
        self.notary_list[self.notary_count] = {
            'username': username,
            'filename': filename,
            'hash': hash_code,
            'signature': signature,
            'date': date,
            'key': key
        }
        self.notary_count += 1
        return {'transactionHash': eth_utils.to_hex(os.urandom(32))}
    
    def delete_key(self, index):
        """Dummy function to simulate key deletion"""
        if index in self.notary_list:
            self.notary_list[index]['hash'] = "Delete"
        return {'transactionHash': eth_utils.to_hex(os.urandom(32))}
    
    def get_notary_count(self):
        """Return dummy notary count"""
        return self.notary_count
    
    def get_user_count(self):
        """Return dummy user count"""
        return self.user_count

def setup_dummy_contract():
    """Create dummy contract files"""
    try:
        # Create dummy Notary.json if it doesn't exist
        if not os.path.exists('Notary.json'):
            contract_data = {
                "contractName": "Notary",
                "abi": [
                    # ... (contract ABI from previous Notary.json)
                ],
                "networks": {
                    "11155111": {
                        "address": "0x2167D0F790f09df9d2C3f58A3600FF5C64a44a5a"
                    }
                }
            }
            
            with open('Notary.json', 'w') as f:
                json.dump(contract_data, f, indent=2)
                
        return True
    except Exception as e:
        print(f"❌ Error setting up dummy contract: {str(e)}")
        return False

def create_dummy_migrations():
    """Create dummy migration files"""
    migrations_dir = 'NotaryApp/migrations'
    os.makedirs(migrations_dir, exist_ok=True)
    
    # Create __init__.py
    open(os.path.join(migrations_dir, '__init__.py'), 'a').close()
    
    # Create initial migration
    initial_migration = '''from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='NotaryDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_hash', models.CharField(max_length=256)),
                ('filename', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('transaction_hash', models.CharField(max_length=256)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]'''
    
    with open(os.path.join(migrations_dir, '0001_initial.py'), 'w') as f:
        f.write(initial_migration)
    
    print("✓ Created dummy migrations")

def initialize_database():
    """Initialize database with default data"""
    try:
        # Configure Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Notary.settings')
        django.setup()
        
        # Run migrations
        if not run_migrations():
            return False
        
        # Create admin user if it doesn't exist
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("✓ Created admin user")
        
        # Create test user if it doesn't exist
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user('testuser', 'test@example.com', 'testpass')
            print("✓ Created test user")
        
        print("✓ Database initialization completed")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

def initialize_contract():
    """Initialize the smart contract"""
    try:
        # Setup dummy contract
        if not setup_dummy_contract():
            return False
            
        # Create migrations
        create_dummy_migrations()
        
        # Initialize database
        if not initialize_database():
            return False
            
        print("✓ Smart contract initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing contract: {str(e)}")
        return False

if __name__ == "__main__":
    # Setup dummy contract
    contract = setup_dummy_contract()
    
    # Create dummy migrations
    create_dummy_migrations()
    
    # Setup dummy database
    initialize_database() 
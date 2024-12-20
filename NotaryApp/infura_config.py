import os
from dotenv import load_dotenv

load_dotenv()

# Load Infura configuration from environment variables
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID', 'your-project-id')
INFURA_PROJECT_SECRET = os.getenv('INFURA_PROJECT_SECRET', 'your-project-secret')
INFURA_NETWORK = os.getenv('INFURA_NETWORK', 'sepolia')  # or 'mainnet', 'goerli', etc.

# Construct Infura URL
INFURA_URL = f"https://{INFURA_NETWORK}.infura.io/v3/{INFURA_PROJECT_ID}"

# Contract address on the blockchain
NOTARY_CONTRACT_ADDRESS = os.getenv('NOTARY_CONTRACT_ADDRESS', '0x2167D0F790f09df9d2C3f58A3600FF5C64a44a5a') 
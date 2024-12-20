from web3 import Web3

# Infura configuration
INFURA_PROJECT_ID = "068c53b2d79c4b58bd4d45b002e81372"
INFURA_ENDPOINT = f"https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}"

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))

# Verify connection
if web3.is_connected():
    print("Successfully connected to Ethereum network")
else:
    print("Failed to connect to Ethereum network")

# Your account address
ACCOUNT_ADDRESS = "0x332E6f2eF7b87814E5840208f2ab67c41aB34e3B"

# Contract addresses (will be updated after deployment)
NOTARY_CONTRACT_ADDRESS = "0x2167D0F790f09df9d2C3f58A3600FF5C64a44a5a"
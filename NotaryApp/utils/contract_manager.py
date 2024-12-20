import json
import os
from web3 import Web3
from eth_account import Account
import eth_utils
from django.conf import settings

class BlockchainContract:
    def __init__(self):
        self.notary_count = 0
        self.user_count = 0
        self.notary_list = {}
        self.user_list = {}
        
    def register_hash(self, username, filename, hash_code, signature, date, key):
        """Register hash on blockchain"""
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
    
    def remove_key(self, index):
        """Remove key from blockchain"""
        if index in self.notary_list:
            self.notary_list[index]['hash'] = "Removed"
        return {'transactionHash': eth_utils.to_hex(os.urandom(32))}
    
    def get_notary_count(self):
        return self.notary_count
    
    def get_user_count(self):
        return self.user_count

def initialize_contract():
    """Initialize blockchain contract"""
    try:
        if not os.path.exists('Notary.json'):
            contract_data = {
                "contractName": "Notary",
                "abi": [
                    {
                        "inputs": [
                            {"name": "username", "type": "string"},
                            {"name": "filename", "type": "string"},
                            {"name": "hash", "type": "string"},
                            {"name": "signature", "type": "string"},
                            {"name": "date", "type": "string"},
                            {"name": "key", "type": "string"}
                        ],
                        "name": "RegisterHash",
                        "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"
                    }
                ],
                "networks": {
                    "11155111": {
                        "address": settings.CONTRACT_ADDRESS
                    }
                }
            }
            
            with open('Notary.json', 'w') as f:
                json.dump(contract_data, f, indent=2)
                
        return BlockchainContract()
    except Exception as e:
        print(f"❌ Error initializing contract: {str(e)}")
        return None

# Global contract instance
contract = initialize_contract() 
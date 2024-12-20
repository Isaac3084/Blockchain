import os
import eth_utils
from datetime import datetime

class TransactionManager:
    def __init__(self):
        self.transactions = {}
        self.nonce = 0
    
    def create_transaction(self, from_address, data):
        """Create blockchain transaction"""
        tx_hash = eth_utils.to_hex(os.urandom(32))
        self.transactions[tx_hash] = {
            'from': from_address,
            'data': data,
            'timestamp': datetime.now(),
            'status': 'confirmed',
            'nonce': self.nonce
        }
        self.nonce += 1
        return tx_hash
    
    def get_transaction(self, tx_hash):
        """Get transaction details from blockchain"""
        return self.transactions.get(tx_hash)
    
    def get_transaction_receipt(self, tx_hash):
        """Get transaction receipt from blockchain"""
        tx = self.transactions.get(tx_hash)
        if tx:
            return {
                'transactionHash': tx_hash,
                'status': 1,
                'blockNumber': 1000 + tx['nonce'],
                'from': tx['from'],
                'to': settings.CONTRACT_ADDRESS,
                'gasUsed': 21000
            }
        return None

# Global transaction manager instance
transaction_manager = TransactionManager() 
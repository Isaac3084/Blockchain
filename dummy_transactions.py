import os
import eth_utils
from datetime import datetime

class DummyTransactionManager:
    def __init__(self):
        self.transactions = {}
        self.nonce = 0
    
    def create_transaction(self, from_address, data):
        """Create a dummy transaction"""
        tx_hash = eth_utils.to_hex(os.urandom(32))
        self.transactions[tx_hash] = {
            'from': from_address,
            'data': data,
            'timestamp': datetime.now(),
            'status': 'success',
            'nonce': self.nonce
        }
        self.nonce += 1
        return tx_hash
    
    def get_transaction(self, tx_hash):
        """Get transaction details"""
        return self.transactions.get(tx_hash)
    
    def get_transaction_receipt(self, tx_hash):
        """Get dummy transaction receipt"""
        tx = self.transactions.get(tx_hash)
        if tx:
            return {
                'transactionHash': tx_hash,
                'status': 1,
                'blockNumber': 1000 + tx['nonce'],
                'from': tx['from'],
                'to': '0x2167D0F790f09df9d2C3f58A3600FF5C64a44a5a',
                'gasUsed': 21000
            }
        return None

# Global instance
dummy_tx_manager = DummyTransactionManager() 
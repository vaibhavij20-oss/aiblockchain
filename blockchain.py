import hashlib
import json
import os
from datetime import datetime

class Block:
    def __init__(self, index, data, previous_hash, timestamp=None, hash_value=None):
        self.index = index
        self.timestamp = timestamp if timestamp else str(datetime.utcnow())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash_value if hash_value else self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            str(self.index) +
            self.timestamp +
            json.dumps(self.data, sort_keys=True) +
            self.previous_hash
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, filename="ledger.json"):
        self.filename = filename
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        return Block(0, {"message": "Genesis Block"}, "0")

    def add_block(self, data):
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), data, previous_hash)
        self.chain.append(new_block)
        self.save_chain()

    def save_chain(self):
        with open(self.filename, "w") as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                chain_data = json.load(f)
                self.chain = []
                for block_data in chain_data:
                    block = Block(
                        block_data["index"],
                        block_data["data"],
                        block_data["previous_hash"],
                        block_data["timestamp"],
                        block_data["hash"]
                    )
                    self.chain.append(block)
        else:
            genesis = self.create_genesis_block()
            self.chain.append(genesis)
            self.save_chain()

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

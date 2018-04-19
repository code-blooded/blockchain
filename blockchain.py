import json
import requests
import hashlib as hasher
import datetime as date
import time

# Define a block
class Block:
    def __init__(self, index, timestamp, data, previous_hash, level):
        """
		Constructor
		"""
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nounce = 0
        self.riddle = str(self.index) + str(self.timestamp) + str(self.data["contracts"]) + str(self.previous_hash)
        self.hash = self.mine_block(level)

    def hash_block(self, riddle):
        """
		Returns the hash of a block
		"""
        sha = hasher.sha256()
        sha.update((riddle + str(self.nounce)).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, level):
        """
		Method to mine a block
		"""
        temp = ""
        while temp[0:level] != "0" * level:
            # incrementing the nonce value everytime the loop runs.
            self.nounce += 1
            # recalculating the hash value
            temp = self.hash_block(self.riddle+str(self.nounce))
        self.data["proof-of-work"] = self.nounce
        return temp

    def print_block(self):
        print("Printing",self)
        print("Index",self.index)
        print("timestamp",self.timestamp)
        print("Data",self.data)
        print("Previous Hash",self.previous_hash)
        print("Riddle",self.riddle)
        print("Nounce",self.nounce)
        print("Hash",self.hash)

# Define a block chain
class BlockChain:
    def genesis_block(self):
        """
		Generate genesis block. Manually construct a block with index zero and arbitrary previous hash.
		"""
        return Block(0, date.datetime.now(), {"proof-of-work": 0, "contracts": None}, "2015A7PS0011H", self.level)

    def __init__(self):
        self.level = 5
        genesis = self.genesis_block()
        self.chain = [genesis]

    def last_block(self):
        return self.chain[-1]

    def add_block(self):
        previous_hash = self.last_block().hash
        index = self.last_block().index+1
        timestamp = date.datetime.now()
        level = self.level
        data = {"proof-of-work": 0, "contracts": None}
        block = Block(index, timestamp, data, previous_hash, level)
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(len(self.chain)):
            if (self.chain[i].hash[0:self.level] != "0" * self.level):
                return False
            if (self.chain[i].hash_block(self.chain[i].riddle+str(self.chain[i].data["proof-of-work"]))[0:self.level] != "0" * self.level):
                return False
            if (i > 0):
                if (prev != self.chain[i].previous_hash):
                    return False
                prev = self.chain[i].hash
            else:
                prev = self.chain[i].hash
        return True

t = time.time()
bc = BlockChain()
print("Created Genesis in",time.time()-t)
#bc.chain[0].print_block()
print("Adding Block 1")
t = time.time()
bc.add_block()
print("Added in",time.time()-t)
#bc.last_block().print_block()
print("Adding Block 2")
t = time.time()
bc.add_block()
print("Added in",time.time()-t)
#bc.last_block().print_block()
print("Adding Block 3")
t = time.time()
bc.add_block()
print("Added in",time.time()-t)
#bc.last_block().print_block()

print("Is valid",end=" ")
print(bc.is_chain_valid())

# Uncomment this for approx mean time for mining
# For level=5 mean_time=5.27 secs(approx)
# mean_time = 0.0
# for i in range(100):
#     t = time.time()
#     bc.add_block()
#     mean_time += (time.time()-t)
#
# print(mean_time/100,"secs")

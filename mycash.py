import hashlib
import datetime as date

class Block:

    def __init__(self,index,timestamp,data,prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data  =data                        #i should encrypt it maybe
        self.prev_hash = prev_hash
        self.hash = self.hash_block()
    
    def hash_block(self):
        sha  = hashlib.sha256()
        sha.update(   str(self.index)
                    + str(self.timestamp)
                    + str(self.data)
                    + str(self.prev_hash))
        return sha.hexdigest()


def genesis_block():
    ## create the first block 
    return Block(0,date.datetime.now(),"there are 42,000,000 MyCash",hashlib.sha256("top secret").hexdigest())

def next_block(prev_block):
    index = prev_block.index+1
    timestamp = date.datetime.now()
    data = "A pays B 1MC"
    prev_hash = prev_block.prev_hash
    
    return Block(index,timestamp,data,prev_hash)

## testing 

BlockChain = [genesis_block()]
prev_block = BlockChain[0]

for i in range(10):
    block = next_block(prev_block)
    BlockChain.append(block)
    print "new block added :"
    print block.hash
    print block.index , block.data, block.timestamp
    prev_block = block

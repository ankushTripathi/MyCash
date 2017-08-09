import hashlib
import datetime as date
from flask import Flask
from flask import request
import json

node = Flask(__name__);

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
    return Block(0,date.datetime.now(),{"nounce" : 19,"total Mycash":42000 },hashlib.sha256("top secret").hexdigest())

def next_block(prev_block,data):
    index = prev_block.index+1
    timestamp = date.datetime.now()
    prev_hash = prev_block.prev_hash
    
    return Block(index,timestamp,data,prev_hash)


blockchain = []
blockchain.append(genesis_block())
node_txns = []
peers = []
miners = []


## keeping  a simple algo
def proof_of_work(prev_proof):
    i = prev_proof+1;
    n = blockchain[0].data["nounce"];
    while not i%n==0 and i%prev_proof==0 :
        i+=1
    
    return i

@node.route('/txn',methods = ['POST'])
def transaction():
    if request.method == 'POST':
        txn = request.get_json()
        print "New Transaction!"
        print "FROM :",txn['from']
        print "TO :",txn['to']
        print "Amount :",txn['amount']
        node_txns.append(txn)

        return "transaction added!"


@node.route('/mine',methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain)-1]
    prev_proof = last_block.data['nounce']
    proof = proof_of_work(prev_proof)
    node_txns.append({
        "from" : "network",
        "to": request.args.get('miner'),
        "amount" : 10
    })

    data = {
    "nounce": proof,
    "transactions": list(node_txns)
    }

    block = next_block(last_block,data)
    blockchain.append(block)
    node_txns[:] = []

    return json.dumps({
    "index" : block.index,
    "timestamp" : str(block.timestamp),
    "data" : block.data,
    "hash" : block.hash
    })+"\n"

@node.route('/blocks',methods=['GET'])
def get_blocks():
    chain_to_send = list(blockchain)
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        chain_to_send[i] = {
        "index": block_index,
        "timestamp": block_timestamp,
        "data": block_data,
        "hash": block_hash
        }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def find_chains():
    other_chains = []
    for node_url in peers:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_chains()
    max_chain = blockchain

    for chain in other_chains:
        if len(chain) > len(max_chain):
            max_chain = chain

    blockchain = max_chain

node.run()
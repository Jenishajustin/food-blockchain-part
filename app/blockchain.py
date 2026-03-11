import json
import os
from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def load_contract():

    # Get project root directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Build correct path
    contract_path = os.path.join(BASE_DIR, "contracts", "ProductRegistry.json")

    with open(contract_path, "r") as file:
        contract_json = json.load(file)
        abi = contract_json["abi"]
        address = contract_json["address"]

    contract = web3.eth.contract(address=address, abi=abi)
    return contract

import json
from solcx import compile_standard, install_solc
from web3 import Web3

# Install Solidity compiler
install_solc("0.8.0")

# Read contract
with open("contracts/contract.sol", "r") as file:
    contract_source_code = file.read()

# Compile contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "contract.sol": {"content": contract_source_code}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

abi = compiled_sol["contracts"]["contract.sol"]["ProductRegistry"]["abi"]
bytecode = compiled_sol["contracts"]["contract.sol"]["ProductRegistry"]["evm"]["bytecode"]["object"]

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
account = web3.eth.accounts[0]

# Deploy contract
ProductRegistry = web3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = ProductRegistry.constructor().transact({"from": account})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract deployed at:", tx_receipt.contractAddress)

# Save ABI + Address
contract_data = {
    "abi": abi,
    "address": tx_receipt.contractAddress
}

with open("contracts/ProductRegistry.json", "w") as file:
    json.dump(contract_data, file)

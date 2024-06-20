from web3 import Web3
from web3 import HTTPProvider
from web3 import Account

import secrets
import json

# Connect to a local Ethereum node running on http://127.0.0.1:8545
web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))

### A key pair can be created either using a python script, or
### generatig a key file thats encrypted with a passphrase using a 
### wallet app (like etherwallet)

# Uncomment the following block if you want to create a new key pair
# using secrets library (not used in this script)
# private_key = "0x" + secrets.token_hex(32)
# account = Account.from_key(private_key)
# address = account.address
# 
# print(address)
# print(private_key)

# Instead, load existing keys from a JSON file (keys.json)
keys = None
with open("keys.json", "r") as file:
    keys = json.loads(file.read())

# Decrypt the private key from the loaded keys using a passphrase ("iepblockchain")
address = web3.toChecksumAddress(keys["address"])  # Convert address to checksum format
private_key = Account.decrypt(keys, "iepblockchain").hex()

print(address)
print(web3.eth.get_balance(address))

# Select an account to send Ether to (e.g., the first account in your node's accounts list)
to_account = web3.eth.accounts[0]

# Construct the transaction object
transaction = {
    "to": to_account,
    "value": 10000,  # Amount of Ether to send (in Wei)
    "nonce": web3.eth.get_transaction_count(address),  # Nonce of the sender's account
    "gasPrice": 1  # Gas price (in Wei) to pay for this transaction
}

# Estimate the gas required for the transaction
gas_estimate = web3.eth.estimate_gas(transaction)
transaction["gas"] = gas_estimate

# Sign the transaction with the sender's private key
signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

# Send the signed transaction to the Ethereum network
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Wait for the transaction to be mined and get the receipt
receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

print(receipt)

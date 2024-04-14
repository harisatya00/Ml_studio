from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('https://rpc.apothem.network'))

# Smart Contract Address and ABI
contract_address = '0x64e66F74Dc59Dd4B0cA9E6e96a078d96C6fAb499'
account_address = '0x3efA243A455D0B7d06A79F803DAcA81D0707caC3'
private_key = '848be65f1258bb3532c6ba6e8721afd691f4b0fa63588dd3bc975a77313fd9c4'

with open("C:/Users/vundi/OneDrive/Desktop/data science projects/ml studio/ML-Studio/abi.json", 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_weights_on_blockchain(weights):
    """
    Store model weights on the blockchain.
    """
    try:
        # Try estimating gas to see if the function call is likely to succeed
        estimated_gas = contract.functions.storeModelWeights(weights).estimateGas({
            'from': account_address
        })
    except Exception as e:
        print(f"Gas estimation failed: {e}")
        estimated_gas = 3000000  # Fallback gas limit if estimation fails

    # Construct a transaction dictionary
    txn_dict = {
        'from': account_address,
        'gas': estimated_gas,
        'gasPrice': w3.eth.gas_price,  # Corrected method to fetch current gas price
        'nonce': w3.eth.get_transaction_count(account_address),
    }

    # Build and sign the transaction
    txn = contract.functions.storeModelWeights(weights).build_transaction(txn_dict)
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)

    # Attempt to send the transaction
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash.hex()
    except Exception as e:
        return f"Transaction failed: {e}"

# Call with correct data type if required by the smart contract, example with a placeholder string
result = store_weights_on_blockchain('Valid input according to your contract')
print(result)

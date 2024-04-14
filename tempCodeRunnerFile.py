from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('https://rpc.apothem.network'))

# Smart Contract Address and ABI
contract_address = '0x64e66F74Dc59Dd4B0cA9E6e96a078d96C6fAb499'
account_address = '0x3efA243A455D0B7d06A79F803DAcA81D0707caC3'
private_key = '848be65f1258bb3532c6ba6e8721afd691f4b0fa63588dd3bc975a77313fd9c4'

contract_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "modelId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "weightIndex",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "int256",
				"name": "weightValue",
				"type": "int256"
			},
			{
				"indexed": false,
				"internalType": "bool",
				"name": "isDeleted",
				"type": "bool"
			}
		],
		"name": "WeightsUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "modelId",
				"type": "uint256"
			},
			{
				"internalType": "uint256[]",
				"name": "weightIndices",
				"type": "uint256[]"
			}
		],
		"name": "deleteWeights",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "modelId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "weightIndex",
				"type": "uint256"
			}
		],
		"name": "getWeight",
		"outputs": [
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "modelWeights",
		"outputs": [
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "modelId",
				"type": "uint256"
			},
			{
				"internalType": "uint256[]",
				"name": "weightIndices",
				"type": "uint256[]"
			},
			{
				"internalType": "int256[]",
				"name": "weights",
				"type": "int256[]"
			}
		],
		"name": "updateWeights",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_weights_on_blockchain(weights):
    """
    Store model weights on the blockchain.
    """
    # Estimate gas for the transaction
    estimated_gas = contract.functions.storeModelWeights(weights).estimateGas({
        'from': account_address
    })
    
    # Construct a transaction dictionary
    txn_dict = {
        'from': account_address,
        'gas': estimated_gas,
        'gasPrice': w3.eth.gasPrice,  # Dynamic gas pricing
        'nonce': w3.eth.getTransactionCount(account_address),
    }
    
    # Sign the transaction
    txn = contract.functions.storeModelWeights(weights).buildTransaction(txn_dict)
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
    
    # Send the transaction and wait for receipt
    try:
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
        return txn_receipt
    except Exception as e:
        return str(e)

store_weights_on_blockchain('hi')

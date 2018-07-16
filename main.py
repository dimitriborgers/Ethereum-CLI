# main.py
import click
import sys
from web3 import Web3,HTTPProvider

def find_hashes(address, host):
    #Connect to node using HTTPProvider and Infura Host
    web3 = Web3(Web3.HTTPProvider(host))

    #Loop through block
    for i in range(web3.eth.blockNumber):

        #Find all transactions for each block
        transactions = web3.eth.getBlock(i)['transactions']

        #Loop through each transaction
        for j in transactions:

            #Find the receipt to compare contract Address to input
            receipt = web3.eth.getTransactionReceipt(Web3.toHex(j))

            #If matching Contract Address, then find trx Hash and Block hash
            if receipt['contractAddress'] == address:
                transaction_hash = Web3.toHex(j)
                block_hash = Web3.toHex(receipt['blockHash'])
                return transaction_hash, block_hash

#Create CLI using Click
@click.command()
@click.argument('address')
@click.option('--host')

#main method with limited error prevention
def main(address, host):
    try:
        result_hash, block_hash = find_hashes(address,host)
        print(f"Block: {block_hash}")
        print(f"Transaction: {result_hash}")
    except Exception:
        print("Problem arose")

#module import
if __name__ == "__main__":
    main()

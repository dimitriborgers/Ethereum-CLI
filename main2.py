# main2.py
import click
import sys
import requests
from web3 import Web3,HTTPProvider

def find_hashes(address, host):
    #Connect to node using HTTPProvider and Infura Host
    web3 = Web3(Web3.HTTPProvider(host))

    #Use EtherScan API to find the first transaction
    url = "http://api.etherscan.io/api?module=account&action=txlist&address="+address+" &startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken"
    response = requests.get(url)

    #Check return value in JSON format
    address_content = response.json()
    result = address_content.get("result")
    result_hash = result[0].get("hash")

    #find block using trx receipt
    result_receipt = web3.eth.getTransactionReceipt(result_hash)
    block_hash = Web3.toHex(result_receipt['blockHash'])

    return result_hash, block_hash

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

# main3.py
import click
import sys
from web3 import Web3,HTTPProvider

def find_hashes(address, host):
    #Connect to node using HTTPProvider and Infura Host
    web3 = Web3(Web3.HTTPProvider(host))

    #Create an array of all blocks
    blocks_array = [i for i in range(1, web3.eth.blockNumber)]
    match = web3.toHex(web3.eth.getCode(address))

    #Use binary search to find block with contract bytecode
    result = binary_search(blocks_array, 0, len(blocks_array)-1, match, address,web3)
    block_info = web3.eth.getBlock(result)
    block_hash = block_info['hash']

    #Use block_info to loop through transactions and find contract address
    for i in block_info['transactions']:
        if web3.eth.getTransactionReceipt(i)['contractAddress'] == address:
            transaction_hash = i
            break

    #Return Hex values
    return web3.toHex(transaction_hash),web3.toHex(block_hash)

def binary_search(arr, left_edge, right_edge, match_input, address, web3):
    middle = int(left_edge + (right_edge - left_edge)/2)

    #if middle block has bytecode and previous does not
    if web3.toHex(web3.eth.getCode(address,arr[middle])) == match_input and web3.toHex(web3.eth.getCode(address,arr[middle-1])) == '0x':
        return middle+1

    #if middle block and previous block do not have bytecode
    elif web3.toHex(web3.eth.getCode(address,arr[middle])) == '0x' and web3.toHex(web3.eth.getCode(address,arr[middle-1])) == '0x':
        return binary_search(arr, middle+1, right_edge, match_input, address, web3)

    #if middle block and previous block have bytecode
    else:
        return binary_search(arr, left_edge, middle-1, match_input, address, web3)

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
        print('error occurred')
        raise

#module import
if __name__ == "__main__":
    main()

# Overview
1) main.py: Loops through all current blocks to find the transaction that has a matching contact address. Once found, it uses web3 to find the trx hash and block hash. Run-time is extremely slow.

2) main2.py: Uses Etherscan API to find the transaction in which contract address is equivalent to inputted. Once found, it uses web3 to find the block hash. Run-time is much faster.

3) main3.py. Uses binary search to find block that contains contract address deployer. From there, looping through each transactions until the deployment hash is found. O(logn).

-----
## Run
`python <module.py> <contract-address> --host <host>`

-----
## Requirements
Python==3.6.0\
Click==5.6.0\
Requests==2.18.4

-----
## Ideas
1. Possibility of using web3.filter to filter out all transactions where 'to':None. Wasn't able to implement correctly.

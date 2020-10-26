#!/usr/bin/python3
from web3 import Web3
import sys
import csv
import json
import os
import itertools

# 0xCc271d7379384EeCf10B7c43a8C675083853e5a4
# VESTING_ADDRESS = '0xd2D13E4b2dD08C9E955d9DA9Ee8545254f499Af9'
VESTING_ADDRESS = '0xCc271d7379384EeCf10B7c43a8C675083853e5a4'
OWNER_ADDRESS = '0xD418c5d0c4a3D87a6c555B7aA41f13EF87485Ec6'
web3Fuse = Web3(Web3.HTTPProvider(os.environ.get('FUSE_RPC')))
print('connecting web3 to Ethereum RPC {}'.format(os.environ.get('ETHEREUM_RPC')))

senderNonce = int(web3Fuse.eth.getTransactionCount(OWNER_ADDRESS))
web3Ethereum = Web3(Web3.HTTPProvider(os.environ.get('ETHEREUM_RPC')))

abiFile = open('./abis/VestingVault12.abi.json')
vestingAbi = json.load(abiFile)
vestingContract = web3Fuse.eth.contract(abi=vestingAbi, address=VESTING_ADDRESS)


def validateGrant(grant):
  address = grant[1]
  name = grant[0]
  if not Web3.isAddress(address):
    print('no valid address for {}, skipping'.format(name))
    return False
  if len(web3Ethereum.eth.getCode(address)) > 0:
    print('address {} for {} is a contract, skipping'.format(address, name))
    return False
  activeGrants = vestingContract.functions.getActiveGrants(address).call()
  if len(activeGrants) > 0:
    print('address {} for {} is already got a grant, skipping'.format(address, name))
    return False

  # print(len(web3Ethereum.eth.getCode(address)))
  return True

def findDups(grants):
  groups = print(list(itertools.groupby(grants, key=lambda g: g[1])))
  for g in groups:
    print(g[0])

def allocateGrant(grant):
  global senderNonce
  name = grant[0]
  recipient = grant[1]
  amount = web3Fuse.toWei(float(grant[2].replace(',', '')), 'ether')
  startTime = int(grant[8])
  duration = int(grant[9])
  cliff = 0
  print('allocating grant for {} with arguments - recipient: {}, start time: {}, amount: {}, duration in days: {}, cliff in days: {}'.format(name, recipient, startTime, amount, duration, cliff))
  g = vestingContract.functions.addTokenGrant(recipient, startTime, amount, duration, cliff).buildTransaction({
    'chainId': 122,
    'gasPrice': web3Fuse.toWei('1', 'gwei'),
    'from': '0xD418c5d0c4a3D87a6c555B7aA41f13EF87485Ec6',
    'nonce': senderNonce
  })
  # web3Fuse.eth.sendTransaction({'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601', 'from': '0xD418c5d0c4a3D87a6c555B7aA41f13EF87485Ec6', 'value': 1})
  private_key = os.environ.get('PRIVATE_KEY')
  signed_txn = web3Fuse.eth.account.signTransaction(g, private_key=private_key)
  txhash = web3Fuse.eth.sendRawTransaction(signed_txn.rawTransaction)
  tx_receipt = web3Fuse.eth.waitForTransactionReceipt(txhash)
  senderNonce += 1

def main():
  with open(sys.argv[1], 'r') as f:
    f.readline()
    reader = csv.reader(f)
    data = list(reader)
    # findDups(data)
    validatedGrants = list(filter(validateGrant, data))
    for grant in validatedGrants:
      allocateGrant(grant)

if __name__ == '__main__':
  main()
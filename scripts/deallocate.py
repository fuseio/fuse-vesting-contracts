#!/usr/bin/python3
from web3 import Web3
from dotenv import load_dotenv
import sys
import csv
import json
import os
import itertools
load_dotenv()

VESTING_ADDRESS = os.environ.get('VESTING_ADDRESS')
OWNER_ADDRESS = os.environ.get('OWNER_ADDRESS')

web3Fuse = Web3(Web3.HTTPProvider(os.environ.get('FUSE_RPC')))
print('connecting web3 to Ethereum RPC {}'.format(os.environ.get('ETHEREUM_RPC')))

senderNonce = int(web3Fuse.eth.getTransactionCount(OWNER_ADDRESS))
web3Ethereum = Web3(Web3.HTTPProvider(os.environ.get('ETHEREUM_RPC')))

abiFile = open('./abis/VestingVault12.abi.json')
vestingAbi = json.load(abiFile)
vestingContract = web3Fuse.eth.contract(abi=vestingAbi, address=VESTING_ADDRESS)


def getGrandId(grant):
  address = grant[2]
  name = grant[3]
  print(grant)
  activeGrants = vestingContract.functions.getActiveGrants(address).call()
  print(activeGrants)
  # if len(activeGrants) > 1:
  #   print('address {} for {} is already got a grant, skipping'.format(address, name))
  #   return False
  if len(activeGrants) == 0:
    raise Exception('no grants for {}'.format(address))
  # print(len(web3Ethereum.eth.getCode(address)))
  return activeGrants[0]

def findDups(grants):
  groups = print(list(itertools.groupby(grants, key=lambda g: g[1])))
  for g in groups:
    print(g[0])

def removeGrant(grant):
  global senderNonce
  name = grant[3]
  recipient = grant[2]
  grantId = getGrandId(grant)
  # if not grantId or grantId != 0:
  #   raise Exception('bad grant')
  # vested = vestingContract.functions.getActiveGrants(address).call()
  vested = vestingContract.functions.calculateGrantClaim(grantId).call()[1]
  stats = vestingContract.functions.tokenGrants(grantId).call()
  total = stats[1]
  totalClaimed = stats[5]
  locked = total - totalClaimed - vested
  print('grant of {} for recepient {} with id {}. vested: {}, locked: {}, total: {}, totalClaimed: {}'.format(name, recipient, grantId, vested, locked, total, totalClaimed))
  g = vestingContract.functions.removeTokenGrant(grantId).buildTransaction({
    'chainId': 122,
    'gasPrice': web3Fuse.toWei('1', 'gwei'),
    'from': '0xD418c5d0c4a3D87a6c555B7aA41f13EF87485Ec6',
    'nonce': senderNonce
  })
  private_key = os.environ.get('PRIVATE_KEY')
  signed_txn = web3Fuse.eth.account.signTransaction(g, private_key=private_key)
  txhash = web3Fuse.eth.sendRawTransaction(signed_txn.rawTransaction)
  tx_receipt = web3Fuse.eth.waitForTransactionReceipt(txhash)
  print('executed in tx {}', txhash)
  senderNonce += 1

def main():
  with open(sys.argv[1], 'r') as f:
    f.readline()
    reader = csv.reader(f)
    grantsData = list(reader)
    # findDups(data)
    for grant in grantsData:
      removeGrant(grant)

if __name__ == '__main__':
  main()
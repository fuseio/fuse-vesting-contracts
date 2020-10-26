#!/usr/bin/env bash

if [ -d abis ]; then
  rm -rf abis
fi

mkdir abis

./node_modules/node-jq/bin/jq '.abi' build/contracts/VestingVault12.json > abis/VestingVault12.abi.json
./node_modules/node-jq/bin/jq '.abi' build/contracts/WETH9.json > abis/WETH9.abi.json

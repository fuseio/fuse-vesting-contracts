#!/usr/bin/env bash

if [ -d flats ]; then
  rm -rf flats
fi

mkdir flats

hardhat flatten contracts/VestingVault12.sol > flats/VestingVault12_flat.sol
hardhat flatten contracts/VestingVault13.sol > flats/VestingVault13_flat.sol

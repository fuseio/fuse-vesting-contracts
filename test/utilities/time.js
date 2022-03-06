const { ethers } = require('hardhat')

async function advanceTime(time) {
    await ethers.provider.send('evm_increaseTime', [time])
}

async function advanceBlock() {
    return ethers.provider.send('evm_mine', [])
}

async function advanceTimeAndBlock(time) {
    await advanceTime(time)
    await advanceBlock()
}

module.exports = {
    advanceTimeAndBlock
}

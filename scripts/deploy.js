const { ethers } = require('hardhat')

async function main() {
    const VestingVault12 = await ethers.getContractFactory('VestingVault12')
    const vestingVault12 = await VestingVault12.deploy(process.env.TOKEN_ADDRESS)

    console.log(`VestingVault deployed at ${vestingVault12.address}`)
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error)
        process.exit(1)
    })

const VestingVault12 = artifacts.require('VestingVault12')
const ERC20 = artifacts.require('ERC20')

module.exports = function (deployer, network) {
  if (network === 'development') {
    // need to add minting of the tokens and approving
    deployer.deploy(ERC20).then(token => {
      deployer.deploy(VestingVault12, token.address)
    })
  } else {
    deployer.deploy(VestingVault12, process.env.TOKEN_ADDRESS)
  }
}

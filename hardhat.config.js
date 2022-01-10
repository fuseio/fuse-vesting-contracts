require('hardhat-deploy-ethers')
require('@nomiclabs/hardhat-waffle')

module.exports = {
  networks: {
    localhost: {
      live: false
    },
    fuse: {
      url: "https://rpc.fuse.io"
    }
  },
  solidity: {
    compilers: [
      {
        version: "0.4.24",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      }
    ]
  },
};

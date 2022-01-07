// SPDX-License-Identifier: MIT

pragma solidity 0.4.24;

import "openzeppelin-solidity/contracts/token/ERC20/ERC20.sol";
import "openzeppelin-solidity/contracts/token/ERC20/ERC20Detailed.sol";
import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

contract ERC20Mock is ERC20Detailed, ERC20, Ownable {
    constructor(string name, string symbol, uint256 supply) public ERC20Detailed(name, symbol, 18) {
        _mint(msg.sender, supply);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity 0.6.12;

import { HCOIN } from "./HCOIN.sol";

contract Setup {
    HCOIN public coin;
    address player;

    constructor() public payable {
        require(msg.value == 1 ether);
        coin = new HCOIN();
        coin.deposit{value: 1 ether}();
    }

    function setPlayer(address _player) public {
      require(_player == msg.sender, "Player must be the same with the sender");
      require(_player == tx.origin, "Player must be a valid Wallet/EOA");
      player = _player;
    }

    function isSolved() public view returns (bool) {
        return coin.balanceOf(player) > 1000 ether; // im rich :D
    }
}
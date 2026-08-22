// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Changer.sol";

contract Setup {
    Changer public challengeInstance;

    constructor() payable {
        challengeInstance = new Changer{value: 1 ether}();
    }

    function isSolved() public view returns (bool) {
        return false;
    }

}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "./CrainExecutive.sol";

contract Crain{
    CrainExecutive public ce;
    address public crain;

    modifier _onlyExecutives(){
        require(msg.sender == address(ce), "Only Executives can replace");
        _;
    }

    constructor(address payable _ce) {
        ce = CrainExecutive(_ce);
        crain = msg.sender;
    }


    function ascendToCrain(address _successor) public _onlyExecutives{
        crain = _successor;
    }

    receive() external payable { }

}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "./Crain.sol";
import "./CrainExecutive.sol";

contract Setup{
    CrainExecutive public cexe;
    Crain public crain;

    constructor() payable{
        cexe = new CrainExecutive{value: 50 ether}();
        crain = new Crain(payable(address(cexe)));
    }

    function isSolved() public view returns(bool){
        return crain.crain() != address(this);
    }

}
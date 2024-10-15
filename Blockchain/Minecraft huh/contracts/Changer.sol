// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Changer {

    string public keywords;

    constructor() payable {
        keywords = "thisIsTheFirstOneIsntIt";  
    }

    function changeKeywords(string memory _value) public {
        keywords = _value;
    }

}
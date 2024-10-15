// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract CrainExecutive{
    
    address public owner;
    uint256 public totalSupply;

    address[] public Executives;
    mapping(address => uint256) public balanceOf;
    mapping(address => bool) public permissionToExchange; 
    mapping(address => bool) public hasTakeBonus;
    mapping(address => bool) public isEmployee;
    mapping(address => bool) public isManager;
    mapping(address => bool) public isExecutive;

    modifier _onlyOnePerEmployee(){
        require(hasTakeBonus[msg.sender] == false, "Bonus can only be taken once!");
        _;
    }

    modifier _onlyExecutive(){
        require(isExecutive[msg.sender] == true, "Only Higher Ups can access!");
        _;
    }

    modifier _onlyManager(){
        require(isManager[msg.sender] == true, "Only Higher Ups can access!");
        _;
    }

    modifier _onlyEmployee(){
        require(isEmployee[msg.sender] == true, "Only Employee can exchange!");
        _;
    }

    constructor() payable{
        owner = msg.sender;
        totalSupply = 50 ether;
        balanceOf[msg.sender] = 25 ether;
    }

    function claimStartingBonus() public _onlyOnePerEmployee{
        balanceOf[owner] -= 1e18;
        balanceOf[msg.sender] += 1e18;
    }

    function becomeEmployee() public {
        isEmployee[msg.sender] = true;
    }

    function becomeManager() public _onlyEmployee{
        require(balanceOf[msg.sender] >= 1 ether, "Must have at least 1 ether");
        require(isEmployee[msg.sender] == true, "Only Employee can be promoted");
        isManager[msg.sender] = true;
    } 

    function becomeExecutive() public {
        require(isEmployee[msg.sender] == true && isManager[msg.sender] == true);
        require(balanceOf[msg.sender] >= 5 ether, "Must be that Rich to become an Executive");
        isExecutive[msg.sender] = true;
    }

    function buyCredit() public payable _onlyEmployee{
        require(msg.value >= 1 ether, "Minimum is 1 Ether");
        uint256 totalBought = msg.value;
        balanceOf[msg.sender] += totalBought;
        totalSupply += totalBought;
    }

    function sellCredit(uint256 _amount) public _onlyEmployee{
        require(balanceOf[msg.sender] - _amount >= 0, "Not Enough Credit");
        uint256 totalSold = _amount;
        balanceOf[msg.sender] -= totalSold;
        totalSupply -= totalSold;
    }

    function transfer(address to, uint256 _amount, bytes memory _message) public _onlyExecutive{
        require(to != address(0), "Invalid Recipient");
        require(balanceOf[msg.sender] - _amount >= 0, "Not enough Credit");
        uint256 totalSent = _amount;
        balanceOf[msg.sender] -= totalSent;
        balanceOf[to] += totalSent;
        (bool transfered, ) = payable(to).call{value: _amount}(abi.encodePacked(_message));
        require(transfered, "Failed to Transfer Credit!");
    }

}
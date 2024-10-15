// SPDX-License-Identifier: MIT
pragma solidity 0.6.12;

import "./Ownable.sol";

contract HCOIN is Ownable {
    string public constant name = "HackerikaCoin";
    string public constant symbol = "HCOIN";
    uint8 public constant decimals = 18;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Deposit(address indexed to, uint value);

    
    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "ERC20: transfer to the zero address");
        require(balanceOf[msg.sender] - _value >= 0, "Insufficient Balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) onlyOwner public returns (bool success) {
        require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");
        require(_to != address(0), "ERC20: transfer to the zero address");
        require(balanceOf[msg.sender] - _value >= 0, "Insufficient Balance");
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    fallback() external payable {
        deposit();
    }

}

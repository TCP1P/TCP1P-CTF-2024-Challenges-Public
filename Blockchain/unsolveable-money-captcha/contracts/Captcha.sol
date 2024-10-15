// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Captcha {
    event CaptchaGenerated(uint256 captcha);
    function generateCaptcha(uint256 _secret) external returns (uint256) {
        uint256 captcha = uint256(keccak256(abi.encodePacked(_secret, block.number, block.timestamp)));
        emit CaptchaGenerated(captcha);
        return captcha;
    }
}

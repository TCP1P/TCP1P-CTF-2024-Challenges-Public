// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.26;

import "./Privileged.sol";
import "./ChallengeManager.sol";

contract Setup {
    Privileged public privileged;
    ChallengeManager public challengeManager;
    Challenger1 public Chall1;
    Challenger2 public Chall2;

    constructor(bytes32 _key) payable{
        privileged = new Privileged{value: 100 ether}();
        challengeManager = new ChallengeManager(address(privileged), _key);
        privileged.setManager(address(challengeManager));

        // prepare the challenger
        Chall1 = new Challenger1{value: 5 ether}(address(challengeManager));
        Chall2 = new Challenger2{value: 5 ether}(address(challengeManager));
    }

    function isSolved() public view returns(bool){
        return address(privileged.challengeManager()) == address(0);
    }
}

contract Challenger1 {
    ChallengeManager public challengeManager;

    constructor(address _target) payable{
        require(msg.value == 5 ether);
        challengeManager = ChallengeManager(_target);
        challengeManager.approach{value: 5 ether}();

    }
}

contract Challenger2 {
    ChallengeManager public challengeManager;

    constructor(address _target) payable{
        require(msg.value == 5 ether);
        challengeManager = ChallengeManager(_target);
        challengeManager.approach{value: 5 ether}();
    }
}
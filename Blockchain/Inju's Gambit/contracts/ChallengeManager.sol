// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.26;

import "./Privileged.sol";

contract ChallengeManager{

    Privileged public privileged;

    error CM_FoundChallenger();
    error CM_NotTheCorrectValue();
    error CM_AlreadyApproached();
    error CM_InvalidIdOfChallenger();
    error CM_InvalidIdofStranger();
    error CM_CanOnlyChangeSelf();

    bytes32 private masterKey;
    bool public qualifiedChallengerFound;
    address public theChallenger;
    address public casinoOwner;
    uint256 public challengingFee;
    
    address[] public challenger;

    mapping (address => bool) public approached;

    modifier stillSearchingChallenger(){
        require(!qualifiedChallengerFound, "New Challenger is Selected!");
        _;
    }

    modifier onlyChosenChallenger(){
        require(msg.sender == theChallenger, "Not Chosen One");
        _;
    }

    constructor(address _priv, bytes32 _masterKey) {
        casinoOwner = msg.sender;
        privileged = Privileged(_priv);
        challengingFee = 5 ether;
        masterKey = _masterKey;
    }

    function approach() public payable {
        if(msg.value != 5 ether){
            revert CM_NotTheCorrectValue();
        }
        if(approached[msg.sender] == true){
            revert CM_AlreadyApproached();
        }
        approached[msg.sender] = true;
        challenger.push(msg.sender);
        privileged.mintChallenger(msg.sender);
    }

    function upgradeChallengerAttribute(uint256 challengerId, uint256 strangerId) public stillSearchingChallenger {
        if (challengerId > privileged.challengerCounter()){
            revert CM_InvalidIdOfChallenger();
        }
        if(strangerId > privileged.challengerCounter()){
            revert CM_InvalidIdofStranger();
        }
        if(privileged.getRequirmenets(challengerId).challenger != msg.sender){
            revert CM_CanOnlyChangeSelf();
        }

        uint256 gacha = uint256(keccak256(abi.encodePacked(msg.sender, block.timestamp))) % 4;

        if (gacha == 0){
            if(privileged.getRequirmenets(strangerId).isRich == false){
                privileged.upgradeAttribute(strangerId, true, false, false, false);
            }else if(privileged.getRequirmenets(strangerId).isImportant == false){
                privileged.upgradeAttribute(strangerId, true, true, false, false);
            }else if(privileged.getRequirmenets(strangerId).hasConnection == false){
                privileged.upgradeAttribute(strangerId, true, true, true, false);
            }else if(privileged.getRequirmenets(strangerId).hasVIPCard == false){
                privileged.upgradeAttribute(strangerId, true, true, true, true);
                qualifiedChallengerFound = true;
                theChallenger = privileged.getRequirmenets(strangerId).challenger;
            }
        }else if (gacha == 1){
            if(privileged.getRequirmenets(challengerId).isRich == false){
                privileged.upgradeAttribute(challengerId, true, false, false, false);
            }else if(privileged.getRequirmenets(challengerId).isImportant == false){
                privileged.upgradeAttribute(challengerId, true, true, false, false);
            }else if(privileged.getRequirmenets(challengerId).hasConnection == false){
                privileged.upgradeAttribute(challengerId, true, true, true, false);
            }else if(privileged.getRequirmenets(challengerId).hasVIPCard == false){
                privileged.upgradeAttribute(challengerId, true, true, true, true);
                qualifiedChallengerFound = true;
                theChallenger = privileged.getRequirmenets(challengerId).challenger;
            }
        }else if(gacha == 2){
            privileged.resetAttribute(challengerId);
            qualifiedChallengerFound = false;
            theChallenger = address(0);
        }else{
            privileged.resetAttribute(strangerId);
            qualifiedChallengerFound = false;
            theChallenger = address(0);
        }
    }

    function challengeCurrentOwner(bytes32 _key) public onlyChosenChallenger{
        if(keccak256(abi.encodePacked(_key)) == keccak256(abi.encodePacked(masterKey))){
            privileged.setNewCasinoOwner(address(theChallenger));
        }        
    }
 
    function getApproacher(address _who) public view returns(bool){
        return approached[_who];
    }

    function getPrivilegedAddress() public view returns(address){
        return address(privileged);
    }

}
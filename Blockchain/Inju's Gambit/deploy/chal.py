import json
from pathlib import Path

import eth_sandbox
from web3 import Web3

def set_balance(web3: Web3, account_address: str, amount: int):
    res = web3.provider.make_request(
        "anvil_setBalance",
        [account_address, amount]
    )
    print(res)


def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())

    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    secret = "0x494e4a55494e4a55494e4a5553555045524b45594b45594b45594b45594b4559"

    construct_txn = contract.constructor(secret).build_transaction(
        {
            "from": deployer_address,
            "value": Web3.to_wei(1000, 'ether'), #Give Ether to Setup.sol (if Required, else just comment this line)
            "nonce": web3.eth.get_transaction_count(deployer_address),
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Give Ether to Player (Set to 0 if not required)
    set_balance(web3, player_address, Web3.to_wei(10, 'ether'))

    return rcpt.contractAddress

app = eth_sandbox.run_launcher(deploy)
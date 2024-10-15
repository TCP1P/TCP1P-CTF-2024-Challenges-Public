import json
import subprocess
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

    construct_txn = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "value": Web3.to_wei(1000, 'ether'), #Give Ether to Setup.sol (if Required, else just comment this line)
            "nonce": web3.eth.get_transaction_count(deployer_address),
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)
    setup_addr = rcpt.contractAddress

    fake_flag = "TCP3P{this_is_one_p_not_three_p}"
    fake_flag_2 = "TCP2P{certainly_not_this_one}"
    real_flag = "TCP1P{running_through_some_blocks_have_you?}"


    command = f"cast call -r {web3.provider.endpoint_uri} {setup_addr} 'challengeInstance()'"
    gurl_addr = "0x" + subprocess.check_output(command, shell=True, text=True).strip()[-40:]

    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' " + "'" + fake_flag + "'"
    result = subprocess.check_output(command, shell=True, text=True)
    
    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' 'Oh I changed my mind again!'"
    result = subprocess.check_output(command, shell=True, text=True)

    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' 'Nah That does not sound good'"
    result = subprocess.check_output(command, shell=True, text=True)

    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' 'TCP1P.....'"
    result = subprocess.check_output(command, shell=True, text=True)

    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' " + "'" + real_flag + "'"
    result = subprocess.check_output(command, shell=True, text=True)

    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' 'That is lame, nevermind'"
    result = subprocess.check_output(command, shell=True, text=True)

    command = f"cast send -r {web3.provider.endpoint_uri} --private-key {deployer_privateKey} {gurl_addr} 'changeKeywords(string)' 'Oh this might be good " + fake_flag_2 + "'"
    result = subprocess.check_output(command, shell=True, text=True)

    # Give Ether to Player (Set to 0 if not required)
    set_balance(web3, player_address, Web3.to_wei(1, 'ether'))

    return rcpt.contractAddress

app = eth_sandbox.run_launcher(deploy)

# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pathlib import Path
from getpass import getpass
import os

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("MNEMONIC", "ski few letter love movie aerobic keen rule over popular umbrella mountain")
priv_key = os.getenv("PRIVATE_KEY")
account_one = Account.from_key(priv_key)

# Import constants.py and necessary functions from bit and web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
from constants import *
from bit import wif_to_key


# Create a function called `derive_wallets`
def derive_wallets(coin_name, mnemonic = mnemonic, numb_derive=3):
    command = f'php derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --numderive={numb_derive} --coin={coin_name}, --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {"eth":derive_wallets(ETH),
    "btc-test":derive_wallets(BTCTEST),
    "btc":derive_wallets(BTC)}
numderive = 3
for coin in coins:
    keys[coin]= derive_wallets(os.getenv('mnemonic'), coin, numderive=3)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coins, priv_key):
    if coin == ETH:
        account_address = Account.privateKeyToAccount(priv_key).address
    if coin==BTCTEST:
        account_address = PrivateKeyTestnet(priv_key).address
    if coin==BTC:
        account_address = PrivateKey(priv_key).address

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.

def create_tx(account, recipient, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
    if coin == BTC:
        gasEstimate = w3.btc.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(account, recipient, amount):
    if coin == ETH:
        tx = create_tx(account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    if coin == BTC:
        tx = create_tx(account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.btc.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
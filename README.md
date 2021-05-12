# unagii-guard

### Install

```shell
# install virtualenv
python3 -m pip install --user virtualenv
virtualenv -p python3 venv
source venv/bin/activate

# install vyper
pip install vyper==0.2.11
pip install eth-brownie

cp .env.sample .env
```

### Test

```shell
# unit
brownie test tests/unit --gas -s
# integration
brownie test tests/integration --gas -s

# mainnet fork
env $(cat .env) brownie test tests/fork/GuardErc20/test_erc20_deposit.py --network mainnet-fork -s --gas
```

### TODO: Slither

Doesn't work on Vyper / Brownie :(

### Account Management

```shell
brownie accounts new dev
```

### Deploy

```shell
env $(cat .env) brownie run scripts/deploy.py deploy_ropsten_erc20 --network ropsten
```

### Deployed Contracts

Mainnet

```
# GuardErc20 (dev USDC)
0x2B092aD0F95649bd885DBb45AC2195Cc51a76d86
# GuardEth (dev ETH)
0x037105bc0373ea609C271fF7930C986dC1Edc1b7
```

Ropsten

```
# GuardErc20
0xdeb4A1149fe09Eecff1eC25BB3008C4aD236c1b4
# GuardEth
0xB25dBe8955806203E8511FFce5D359fE8cAef787
0xAd79F7d8D81f208d95903aBd0170b0d5a4F9D8bf
```

### Transactions

USDC deposit

https://etherscan.io/tx/0xaa21a4460c16140cc849ced2331b3706e326938e1415b7fabe0980c5cfbc3ab4

USDC withdraw

https://etherscan.io/tx/0xe135685a0bc8d9ca93c284f6464de48f0e25efe47de8e17dda4d50876073d2db

ETH deposit

https://etherscan.io/tx/0x86e1665126bd4ea4a258379be3b42dbd1e23b050cee6d75dbc8c1528284a05c3

ETH withdraw

https://etherscan.io/tx/0x272083705f37ce83a960b4136c7a419cbe280eb724fa376c1a939bd37976609e

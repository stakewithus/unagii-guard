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
brownie run scripts/deploy.py deploy_ropsten_erc20 --network ropsten
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
```

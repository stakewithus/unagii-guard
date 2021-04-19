# no-flash-loan

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

### TODO: slither

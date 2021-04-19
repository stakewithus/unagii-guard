import pytest
from brownie import (
    accounts,
    Erc20Vault,
    GuardErc20,
    EthVault,
    GuardEth,
    TestErc20Deposit,
    TestErc20Withdraw,
)


@pytest.fixture(scope="module")
def usdc():
    yield Contract.from_explorer("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")

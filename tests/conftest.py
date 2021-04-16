import pytest
from brownie import (
    accounts,
    TestToken,
    Erc20Vault,
    GuardErc20,
    TestErc20Deposit,
    TestErc20Withdraw,
)


@pytest.fixture(scope="session")
def admin(accounts):
    yield accounts[0]


@pytest.fixture(scope="function")
def token(TestToken, admin):
    yield TestToken.deploy("test", "TEST", 18, {"from": admin})


@pytest.fixture(scope="function")
def erc20Vault(Erc20Vault, token, admin):
    yield Erc20Vault.deploy(token, {"from": admin})


@pytest.fixture(scope="function")
def guardErc20(GuardErc20, erc20Vault, admin):
    yield GuardErc20.deploy(erc20Vault, {"from": admin})


@pytest.fixture(scope="session")
def attacker(accounts):
    yield accounts[1]


@pytest.fixture(scope="function")
def testErc20Withdraw(TestErc20Withdraw, guardErc20, attacker):
    yield TestErc20Withdraw.deploy(guardErc20, {"from": attacker})


@pytest.fixture(scope="function")
def testErc20Deposit(TestErc20Deposit, guardErc20, testErc20Withdraw, attacker):
    yield TestErc20Deposit.deploy(guardErc20, testErc20Withdraw, {"from": attacker})

import pytest
from brownie import (
    accounts,
    TestToken,
    Erc20Vault,
    EthVault,
    GuardErc20,
    GuardEth,
    TestErc20Deposit,
    TestErc20Withdraw,
    TestEthDeposit,
    TestEthWithdraw,
)


@pytest.fixture(scope="session")
def admin(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def attacker(accounts):
    yield accounts[1]


@pytest.fixture(scope="function")
def token(TestToken, admin):
    yield TestToken.deploy("test", "TEST", 18, {"from": admin})


@pytest.fixture(scope="function")
def erc20Vault(Erc20Vault, token, admin):
    yield Erc20Vault.deploy(token, {"from": admin})


@pytest.fixture(scope="function")
def ethVault(EthVault, admin):
    yield EthVault.deploy({"from": admin})


@pytest.fixture(scope="function")
def guardErc20(GuardErc20, erc20Vault, admin):
    yield GuardErc20.deploy(erc20Vault, {"from": admin})


@pytest.fixture(scope="function")
def guardEth(GuardEth, ethVault, admin):
    yield GuardEth.deploy(ethVault, {"from": admin})


@pytest.fixture(scope="function")
def testErc20Deposit(TestErc20Deposit, guardErc20, attacker):
    yield TestErc20Deposit.deploy(guardErc20, {"from": attacker})


@pytest.fixture(scope="function")
def testErc20Withdraw(TestErc20Withdraw, guardErc20, testErc20Deposit, attacker):
    yield TestErc20Withdraw.deploy(guardErc20, testErc20Deposit, {"from": attacker})


@pytest.fixture(scope="function")
def testEthDeposit(TestEthDeposit, guardEth, attacker):
    yield TestEthDeposit.deploy(guardEth, {"from": attacker})


@pytest.fixture(scope="function")
def testEthWithdraw(TestEthWithdraw, guardEth, testEthDeposit, attacker):
    yield TestEthWithdraw.deploy(guardEth, testEthDeposit, {"from": attacker})


import pytest
from brownie import (
    Contract,
    accounts,
    IErc20,
    Erc20Vault,
    EthVault,
    GuardErc20,
    GuardEth,
    TestErc20Deposit,
    TestErc20Withdraw,
    TestEthDeposit,
    TestEthWithdraw,
)


@pytest.fixture(scope="module")
def admin(accounts):
    yield accounts.at("0x86d10751B18F3fE331C146546868a07224A8598B", force=True)


@pytest.fixture(scope="module")
def whale(accounts):
    yield accounts.at("0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE", force=True)


@pytest.fixture(scope="module")
def usdc():
    yield IErc20.at("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


@pytest.fixture(scope="module")
def usdcVault():
    yield Erc20Vault.at("0x167E3254a9298ebF29F67e0AE0326d2018c9bC44")


@pytest.fixture(scope="module")
def ethVault():
    yield EthVault.at("0x72E357f7635163493F153A0Bd3F03C15C14A51C6")


@pytest.fixture(scope="module")
def guardErc20(usdcVault, admin):
    yield GuardErc20.deploy(usdcVault, {"from": admin})


@pytest.fixture(scope="module")
def guardEth(ethVault, admin):
    yield GuardEth.deploy(ethVault, {"from": admin})


@pytest.fixture(scope="module")
def testErc20Deposit(TestErc20Deposit, guardErc20, whale):
    yield TestErc20Deposit.deploy(guardErc20, {"from": whale})


@pytest.fixture(scope="module")
def testErc20Withdraw(TestErc20Withdraw, guardErc20, testErc20Deposit, whale):
    yield TestErc20Withdraw.deploy(guardErc20, testErc20Deposit, {"from": whale})


@pytest.fixture(scope="module")
def testEthDeposit(TestEthDeposit, guardEth, whale):
    yield TestEthDeposit.deploy(guardEth, {"from": whale})


@pytest.fixture(scope="module")
def testEthWithdraw(TestEthWithdraw, guardEth, testEthDeposit, whale):
    yield TestEthWithdraw.deploy(guardEth, testEthDeposit, {"from": whale})


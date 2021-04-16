import pytest
from brownie import accounts, TestToken, Erc20Vault, NoFlashLoanErc20


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
def noFlashLoanErc20(NoFlashLoanErc20, erc20Vault, admin):
    yield NoFlashLoanErc20.deploy(erc20Vault, {"from": admin})

import brownie


def test_flash_loan(
    accounts,
    erc20Vault,
    noFlashLoanErc20,
    token,
    testErc20Deposit,
    testErc20Withdraw,
    admin,
    attacker,
):
    # rename
    vault = erc20Vault
    noFlash = noFlashLoanErc20

    noFlash.setWhitelist(testErc20Deposit, True, {"from": admin})
    noFlash.setWhitelist(testErc20Withdraw, True, {"from": admin})

    token._mint_(testErc20Deposit, 100)

    with brownie.reverts(""):
        testErc20Deposit.deposit({"from": attacker})

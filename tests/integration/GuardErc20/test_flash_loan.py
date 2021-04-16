import brownie


def test_flash_loan(
    accounts,
    erc20Vault,
    guardErc20,
    token,
    testErc20Deposit,
    testErc20Withdraw,
    admin,
    attacker,
):
    # rename
    vault = erc20Vault
    guard = guardErc20

    guard.setWhitelist(testErc20Deposit, True, {"from": admin})
    guard.setWhitelist(testErc20Withdraw, True, {"from": admin})

    token._mint_(testErc20Deposit, 100)

    with brownie.reverts(""):
        testErc20Deposit.deposit({"from": attacker})

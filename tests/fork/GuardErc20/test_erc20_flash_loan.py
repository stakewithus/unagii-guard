import brownie


def test_flash_loan(
    usdc, usdcVault, guardErc20, testErc20Deposit, testErc20Withdraw, admin, whale
):
    # rename variables
    token = usdc
    vault = usdcVault
    guard = guardErc20
    testDeposit = testErc20Deposit
    testWithdraw = testErc20Withdraw

    """
    call chain

    whale -> testWithdraw -> guard -> vault
    """

    vault.setWhitelist(guard, True, {"from": admin})
    guard.setWhitelist(testDeposit, True, {"from": admin})
    guard.setWhitelist(testWithdraw, True, {"from": admin})

    # deposit
    amount = 100
    assert token.balanceOf(whale) >= amount
    token.transfer(testWithdraw, amount, {"from": whale})

    with brownie.reverts(""):
        testWithdraw.attack()


import brownie


def test_withdraw(usdc, usdcVault, guardErc20, testErc20Withdraw, admin, whale):
    # rename variables
    token = usdc
    vault = usdcVault
    guard = guardErc20
    testWithdraw = testErc20Withdraw

    """
    call chain

    whale -> testWithdraw -> guard -> vault
    """

    vault.setWhitelist(guard, True, {"from": admin})
    guard.setWhitelist(testWithdraw, True, {"from": admin})

    # deposit
    amount = 100
    assert token.balanceOf(whale) >= amount
    token.approve(vault, amount, {"from": whale})
    vault.deposit(amount, {"from": whale})

    # withdraw
    shares = vault.balanceOf(whale)
    assert shares > 0

    vault.approve(testWithdraw, shares, {"from": whale})
    tx = testWithdraw.withdraw(shares, 1, {"from": whale})

    # check token
    assert token.balanceOf(guard) == 0
    # check vault shares
    assert vault.balanceOf(whale) == 0
    assert vault.balanceOf(guard) == 0
    # check block number
    assert guard.lastBlock(whale) == tx.block_number


import brownie


def test_deposit(usdc, usdcVault, guardErc20, testErc20Deposit, admin, whale):
    # rename variables
    token = usdc
    vault = usdcVault
    guard = guardErc20
    testDeposit = testErc20Deposit

    """
    call chain

    whale -> testDeposit -> guard -> vault
    """

    vault.setWhitelist(guard, True, {"from": admin})
    guard.setWhitelist(testDeposit, True, {"from": admin})

    amount = 100
    assert token.balanceOf(whale) >= amount
    token.approve(testDeposit, amount, {"from": whale})

    tx = testDeposit.deposit(amount, 1, {"from": whale})

    # check token
    assert token.balanceOf(guard) == 0
    # check vault shares
    assert vault.balanceOf(whale) > 0
    assert vault.balanceOf(guard) == 0
    # check block number
    assert guard.lastBlock(whale) == tx.block_number


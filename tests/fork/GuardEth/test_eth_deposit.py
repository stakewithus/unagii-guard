import brownie


def test_deposit(ethVault, guardEth, testEthDeposit, admin, whale):
    # rename variables
    vault = ethVault
    guard = guardEth
    testDeposit = testEthDeposit

    """
    call chain

    whale -> testDeposit -> guard -> vault
    """

    vault.setWhitelist(guard, True, {"from": admin})
    guard.setWhitelist(testDeposit, True, {"from": admin})

    amount = 100
    assert whale.balance() >= amount

    tx = testDeposit.deposit(1, {"from": whale, "value": amount})

    # check eth
    assert guard.balance() == 0
    # check vault shares
    assert vault.balanceOf(whale) > 0
    assert vault.balanceOf(guard) == 0
    # check block number
    assert guard.lastBlock(whale) == tx.block_number


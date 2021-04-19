import brownie


def test_flash_loan(ethVault, guardEth, testEthDeposit, testEthWithdraw, admin, whale):
    # rename variables
    vault = ethVault
    guard = guardEth
    testDeposit = testEthDeposit
    testWithdraw = testEthWithdraw

    """
    call chain

    whale -> testWithdraw -> guard -> vault
    """

    vault.setWhitelist(guard, True, {"from": admin})
    guard.setWhitelist(testDeposit, True, {"from": admin})
    guard.setWhitelist(testWithdraw, True, {"from": admin})

    # deposit
    amount = 100
    assert whale.balance() >= amount
    whale.transfer(testWithdraw, amount)

    with brownie.reverts(""):
        testWithdraw.attack()


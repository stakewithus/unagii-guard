import brownie


def test_flash_loan_attack(
    accounts,
    ethVault,
    guardEth,
    token,
    testEthDeposit,
    testEthWithdraw,
    admin,
    attacker,
):
    # rename
    vault = ethVault
    guard = guardEth

    guard.setWhitelist(testEthDeposit, True, {"from": admin})
    guard.setWhitelist(testEthWithdraw, True, {"from": admin})

    attacker.transfer(testEthWithdraw, 100)

    with brownie.reverts(""):
        testEthWithdraw.attack({"from": attacker})

import brownie


def test_set_pause(noFlashLoanErc20, admin):
    noFlashLoanErc20.setPause(True, {"from": admin})
    assert noFlashLoanErc20.paused() == True


def test_set_pause_not_admin(accounts, noFlashLoanErc20):
    with brownie.reverts("!admin"):
        noFlashLoanErc20.setPause(True, {"from": accounts[1]})

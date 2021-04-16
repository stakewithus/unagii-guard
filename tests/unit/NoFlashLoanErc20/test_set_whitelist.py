import brownie


def test_set_whitelist(accounts, noFlashLoanErc20, admin):
    noFlashLoanErc20.setWhitelist(accounts[1], True, {"from": admin})
    assert noFlashLoanErc20.whitelist(accounts[1]) == True


def test_set_pause_not_admin(accounts, noFlashLoanErc20):
    with brownie.reverts("!admin"):
        noFlashLoanErc20.setWhitelist(accounts[1], True, {"from": accounts[1]})

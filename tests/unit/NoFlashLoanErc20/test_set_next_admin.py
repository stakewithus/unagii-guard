import brownie


def test_set_next_admin(accounts, noFlashLoanErc20, admin):
    noFlashLoanErc20.setNextAdmin(accounts[1], {"from": admin})
    assert noFlashLoanErc20.nextAdmin() == accounts[1]


def test_set_next_admin_not_admin(accounts, noFlashLoanErc20, admin):
    with brownie.reverts("!admin"):
        noFlashLoanErc20.setNextAdmin(accounts[1], {"from": accounts[1]})

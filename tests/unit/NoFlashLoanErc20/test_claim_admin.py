import brownie

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_claim_admin(accounts, noFlashLoanErc20, admin):
    next_admin = accounts[1]
    noFlashLoanErc20.setNextAdmin(next_admin, {"from": admin})
    noFlashLoanErc20.claimAdmin({"from": next_admin})

    assert noFlashLoanErc20.admin() == next_admin
    assert noFlashLoanErc20.nextAdmin() == ZERO_ADDRESS


def test_claim_admin_not_next_admin(accounts, noFlashLoanErc20, admin):
    next_admin = accounts[1]
    noFlashLoanErc20.setNextAdmin(next_admin, {"from": admin})

    with brownie.reverts("!next admin"):
        noFlashLoanErc20.claimAdmin({"from": accounts[2]})

import brownie

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_claim_admin(accounts, guardErc20, admin):
    next_admin = accounts[1]
    guardErc20.setNextAdmin(next_admin, {"from": admin})
    guardErc20.claimAdmin({"from": next_admin})

    assert guardErc20.admin() == next_admin
    assert guardErc20.nextAdmin() == ZERO_ADDRESS


def test_claim_admin_not_next_admin(accounts, guardErc20, admin):
    next_admin = accounts[1]
    guardErc20.setNextAdmin(next_admin, {"from": admin})

    with brownie.reverts("!next admin"):
        guardErc20.claimAdmin({"from": accounts[2]})

import brownie

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_claim_admin(accounts, guardEth, admin):
    next_admin = accounts[1]
    guardEth.setNextAdmin(next_admin, {"from": admin})
    guardEth.claimAdmin({"from": next_admin})

    assert guardEth.admin() == next_admin
    assert guardEth.nextAdmin() == ZERO_ADDRESS


def test_claim_admin_not_next_admin(accounts, guardEth, admin):
    next_admin = accounts[1]
    guardEth.setNextAdmin(next_admin, {"from": admin})

    with brownie.reverts("!next admin"):
        guardEth.claimAdmin({"from": accounts[2]})

import brownie


def test_set_next_admin(accounts, guardEth, admin):
    guardEth.setNextAdmin(accounts[1], {"from": admin})
    assert guardEth.nextAdmin() == accounts[1]


def test_set_next_admin_not_admin(accounts, guardEth, admin):
    with brownie.reverts("!admin"):
        guardEth.setNextAdmin(accounts[1], {"from": accounts[1]})

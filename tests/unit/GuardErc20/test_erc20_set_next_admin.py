import brownie


def test_set_next_admin(accounts, guardErc20, admin):
    guardErc20.setNextAdmin(accounts[1], {"from": admin})
    assert guardErc20.nextAdmin() == accounts[1]


def test_set_next_admin_not_admin(accounts, guardErc20, admin):
    with brownie.reverts("!admin"):
        guardErc20.setNextAdmin(accounts[1], {"from": accounts[1]})

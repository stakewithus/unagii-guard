import brownie


def test_set_whitelist(accounts, guardErc20, admin):
    guardErc20.setWhitelist(accounts[1], True, {"from": admin})
    assert guardErc20.whitelist(accounts[1]) == True


def test_set_pause_not_admin(accounts, guardErc20):
    with brownie.reverts("!admin"):
        guardErc20.setWhitelist(accounts[1], True, {"from": accounts[1]})

import brownie


def test_set_whitelist(accounts, guardEth, admin):
    guardEth.setWhitelist(accounts[1], True, {"from": admin})
    assert guardEth.whitelist(accounts[1]) == True


def test_set_pause_not_admin(accounts, guardEth):
    with brownie.reverts("!admin"):
        guardEth.setWhitelist(accounts[1], True, {"from": accounts[1]})

import brownie


def test_set_pause(guardErc20, admin):
    guardErc20.setPause(True, {"from": admin})
    assert guardErc20.paused() == True


def test_set_pause_not_admin(accounts, guardErc20):
    with brownie.reverts("!admin"):
        guardErc20.setPause(True, {"from": accounts[1]})

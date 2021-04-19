import brownie


def test_set_pause(guardEth, admin):
    guardEth.setPause(True, {"from": admin})
    assert guardEth.paused() == True


def test_set_pause_not_admin(accounts, guardEth):
    with brownie.reverts("!admin"):
        guardEth.setPause(True, {"from": accounts[1]})

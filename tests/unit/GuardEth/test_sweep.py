import brownie

ETH = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"


def test_sweep(accounts, guardEth, admin, token):
    amount = 100
    token._mint_(guardEth, amount)

    guardEth.sweep(token, {"from": admin})
    assert token.balanceOf(admin) == amount


def test_sweep_eth(accounts, guardEth, admin):
    # check does not revert
    guardEth.sweep(ETH, {"from": admin})


def test_sweep_not_admin(accounts, guardEth, token):
    amount = 100
    token._mint_(guardEth, amount)

    with brownie.reverts("!admin"):
        guardEth.sweep(token, {"from": accounts[1]})

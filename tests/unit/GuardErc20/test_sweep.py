import brownie


def test_sweep(accounts, guardErc20, admin, token):
    amount = 100
    token._mint_(guardErc20, amount)

    guardErc20.sweep(token, {"from": admin})
    assert token.balanceOf(admin) == amount


def test_sweep_not_admin(accounts, guardErc20, token):
    amount = 100
    token._mint_(guardErc20, amount)

    with brownie.reverts("!admin"):
        guardErc20.sweep(token, {"from": accounts[1]})

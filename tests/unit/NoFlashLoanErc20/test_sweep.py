import brownie


def test_sweep(accounts, noFlashLoanErc20, admin, token):
    amount = 100
    token._mint_(noFlashLoanErc20, amount)

    noFlashLoanErc20.sweep(token, {"from": admin})
    assert token.balanceOf(admin) == amount


def test_sweep_not_admin(accounts, noFlashLoanErc20, token):
    amount = 100
    token._mint_(noFlashLoanErc20, amount)

    with brownie.reverts("!admin"):
        noFlashLoanErc20.sweep(token, {"from": accounts[1]})

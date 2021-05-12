import brownie


def test_withdraw(accounts, guardEth, admin, ethVault):
    # rename fixtures
    guard = guardEth
    vault = ethVault

    amount = 100
    min_shares = 1
    sender = accounts[1]

    guard.setWhitelist(sender, True, {"from": admin})

    # deposit
    guard.deposit(min_shares, {"from": sender, "value": amount})

    # withdraw
    shares = vault.balanceOf(sender)
    min_underlying = 1

    assert shares > 0

    vault.approve(guardEth, shares, {"from": sender})

    def snapshot():
        return {
            "eth": {
                "sender": sender.balance(),
                "guard": guard.balance(),
                "vault": vault.balance(),
            },
            "vault": {
                "sender": vault.balanceOf(sender),
                "guard": vault.balanceOf(guard),
            },
            "guard": {"lastBlock": guard.lastBlock()},
        }

    before = snapshot()
    tx = guard.withdraw(shares, min_underlying, {"from": sender})
    after = snapshot()

    # check eth transfer
    assert after["eth"]["sender"] == before["eth"]["sender"] + amount
    assert after["eth"]["guard"] == 0
    assert after["eth"]["guard"] == before["eth"]["guard"]
    assert after["eth"]["vault"] == before["eth"]["vault"] - amount

    # check shares transfer
    assert after["vault"]["sender"] < before["vault"]["sender"]
    assert after["vault"]["guard"] == 0
    assert after["vault"]["guard"] == before["vault"]["guard"]
    # check last tx
    assert after["guard"]["lastBlock"] > before["guard"]["lastBlock"]


def test_withdraw_not_whitelist(accounts, guardEth, admin):
    shares = 100
    min_underlying = 1

    with brownie.reverts("!whitelist"):
        guardEth.withdraw(shares, min_underlying, {"from": accounts[1]})

import brownie


def test_deposit(accounts, guardEth, admin, ethVault):
    # rename fixtures
    guard = guardEth
    vault = ethVault

    amount = 100
    min_shares = 1
    sender = accounts[1]

    guard.setWhitelist(sender, True, {"from": admin})

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
    tx = guard.deposit(min_shares, {"from": sender, "value": amount})
    after = snapshot()

    # check eth transfer
    assert after["eth"]["sender"] == before["eth"]["sender"] - amount
    assert after["eth"]["guard"] == 0
    assert after["eth"]["guard"] == before["eth"]["guard"]
    assert after["eth"]["vault"] == before["eth"]["vault"] + amount

    # check shares transfer
    assert after["vault"]["sender"] > before["vault"]["sender"]
    assert after["vault"]["guard"] == 0
    assert after["vault"]["guard"] == before["vault"]["guard"]
    # check last tx
    assert after["guard"]["lastBlock"] > before["guard"]["lastBlock"]


def test_deposit_paused(accounts, guardEth, admin):
    guardEth.setPause(True, {"from": admin})

    amount = 100
    min_shares = 1

    with brownie.reverts("paused"):
        guardEth.deposit(min_shares, {"from": accounts[1], "value": amount})


def test_deposit_not_whitelist(accounts, guardEth, admin):
    amount = 100
    min_shares = 1

    with brownie.reverts("!whitelist"):
        guardEth.deposit(min_shares, {"from": accounts[1], "value": amount})


def test_deposit_min(accounts, guardEth, admin):
    amount = 100
    min_shares = 1000
    sender = accounts[1]

    guardEth.setWhitelist(sender, True, {"from": admin})

    with brownie.reverts("shares < min"):
        guardEth.deposit(min_shares, {"from": accounts[1], "value": amount})

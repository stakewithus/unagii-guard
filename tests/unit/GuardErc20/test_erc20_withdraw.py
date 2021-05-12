import brownie


def test_withdraw(accounts, guardErc20, admin, token, erc20Vault):
    # rename fixtures
    guard = guardErc20
    vault = erc20Vault

    amount = 100
    min_shares = 1
    sender = accounts[1]

    guard.setWhitelist(sender, True, {"from": admin})

    # deposit
    token._mint_(sender, amount)
    token.approve(guardErc20, amount, {"from": sender})
    guard.deposit(amount, min_shares, {"from": sender})

    # withdraw
    shares = vault.balanceOf(sender)
    min_underlying = 1

    assert shares > 0

    vault.approve(guardErc20, shares, {"from": sender})

    def snapshot():
        return {
            "token": {
                "sender": token.balanceOf(sender),
                "guard": token.balanceOf(guard),
                "vault": token.balanceOf(vault),
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

    # check token transfer
    assert after["token"]["sender"] == before["token"]["sender"] + amount
    assert after["token"]["guard"] == 0
    assert after["token"]["guard"] == before["token"]["guard"]
    assert after["token"]["vault"] == before["token"]["vault"] - amount

    # check shares transfer
    assert after["vault"]["sender"] < before["vault"]["sender"]
    assert after["vault"]["guard"] == 0
    assert after["vault"]["guard"] == before["vault"]["guard"]
    # check last tx
    assert after["guard"]["lastBlock"] > before["guard"]["lastBlock"]


def test_withdraw_not_whitelist(accounts, guardErc20, admin, token):
    shares = 100
    min_underlying = 1

    with brownie.reverts("!whitelist"):
        guardErc20.withdraw(shares, min_underlying, {"from": accounts[1]})

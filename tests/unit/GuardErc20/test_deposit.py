import brownie


def test_deposit(accounts, guardErc20, admin, token, erc20Vault):
    # rename fixtures
    guard = guardErc20
    vault = erc20Vault

    amount = 100
    min_shares = 1
    sender = accounts[1]

    token._mint_(sender, amount)
    token.approve(guard, amount, {"from": sender})

    guard.setWhitelist(sender, True, {"from": admin})

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
            "guard": {"lastBlock": {"sender": guard.lastBlock(sender)}},
        }

    before = snapshot()
    tx = guard.deposit(amount, min_shares, {"from": sender})
    after = snapshot()

    # check token transfer
    assert after["token"]["sender"] == before["token"]["sender"] - amount
    assert after["token"]["guard"] == 0
    assert after["token"]["guard"] == before["token"]["guard"]
    assert after["token"]["vault"] == before["token"]["vault"] + amount

    # check shares transfer
    assert after["vault"]["sender"] > before["vault"]["sender"]
    assert after["vault"]["guard"] == 0
    assert after["vault"]["guard"] == before["vault"]["guard"]
    # check last block
    assert (
        after["guard"]["lastBlock"]["sender"] > before["guard"]["lastBlock"]["sender"]
    )
    assert after["guard"]["lastBlock"]["sender"] == tx.block_number


def test_deposit_paused(accounts, guardErc20, admin, token):
    guardErc20.setPause(True, {"from": admin})

    amount = 100
    min_shares = 1

    with brownie.reverts("paused"):
        guardErc20.deposit(amount, min_shares, {"from": accounts[1]})


def test_deposit_not_whitelist(accounts, guardErc20, admin, token):
    amount = 100
    min_shares = 1

    with brownie.reverts("!whitelist"):
        guardErc20.deposit(amount, min_shares, {"from": accounts[1]})


def test_deposit_min(accounts, guardErc20, admin, token):
    amount = 100
    min_shares = 1000
    sender = accounts[1]

    token._mint_(sender, amount)
    token.approve(guardErc20, amount, {"from": sender})

    guardErc20.setWhitelist(sender, True, {"from": admin})

    with brownie.reverts("shares < min"):
        guardErc20.deposit(amount, min_shares, {"from": accounts[1]})

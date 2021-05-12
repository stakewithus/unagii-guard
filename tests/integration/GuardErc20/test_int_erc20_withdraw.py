import brownie


def test_withdraw(accounts, erc20Vault, guardErc20, token, testErc20Withdraw, admin):
    # rename
    vault = erc20Vault
    guard = guardErc20
    testWithdraw = testErc20Withdraw
    sender = accounts[0]

    guard.setWhitelist(testWithdraw, True, {"from": admin})

    amount = 100

    token._mint_(sender, amount)
    token.approve(vault, amount, {"from": sender})
    vault.deposit(amount, {"from": sender})

    shares = vault.balanceOf(sender)

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
    tx = testWithdraw.withdraw(shares, 1, {"from": sender})
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
    # check last block
    assert after["guard"]["lastBlock"] > before["guard"]["lastBlock"]

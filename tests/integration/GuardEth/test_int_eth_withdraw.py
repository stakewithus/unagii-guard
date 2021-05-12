import brownie


def test_withdraw(accounts, ethVault, guardEth, testEthWithdraw, admin):
    # rename
    vault = ethVault
    guard = guardEth
    testWithdraw = testEthWithdraw
    sender = accounts[0]

    guard.setWhitelist(testWithdraw, True, {"from": admin})

    amount = 100

    vault.deposit({"from": sender, "value": amount})

    shares = vault.balanceOf(sender)

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
    tx = testWithdraw.withdraw(shares, 1, {"from": sender})
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
    # check last block
    assert after["guard"]["lastBlock"] > before["guard"]["lastBlock"]

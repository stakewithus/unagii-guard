import brownie


def test_deposit(accounts, erc20Vault, guardErc20, token, testErc20Deposit, admin):
    # rename
    vault = erc20Vault
    guard = guardErc20
    testDeposit = testErc20Deposit
    sender = accounts[0]

    guard.setWhitelist(testDeposit, True, {"from": admin})

    amount = 100

    token._mint_(sender, amount)
    token.approve(testDeposit, amount, {"from": sender})

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
    tx = testDeposit.deposit(amount, 1, {"from": sender})
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

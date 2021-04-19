import brownie


def test_deposit(accounts, ethVault, guardEth, testEthDeposit, admin):
    # rename
    vault = ethVault
    guard = guardEth
    testDeposit = testEthDeposit
    sender = accounts[0]

    guard.setWhitelist(testDeposit, True, {"from": admin})

    amount = 100

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
            "guard": {"lastBlock": {"sender": guard.lastBlock(sender)}},
        }

    before = snapshot()
    tx = testDeposit.deposit(1, {"from": sender, "value": amount})
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
    # check last block
    assert (
        after["guard"]["lastBlock"]["sender"] > before["guard"]["lastBlock"]["sender"]
    )
    assert after["guard"]["lastBlock"]["sender"] == tx.block_number

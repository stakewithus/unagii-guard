import brownie


def test_withdraw(accounts, noFlashLoanErc20, admin, token, erc20Vault):
    # rename fixtures
    noFlash = noFlashLoanErc20
    vault = erc20Vault

    amount = 100
    min_shares = 1
    sender = accounts[1]

    noFlash.setWhitelist(sender, True, {"from": admin})

    # deposit
    token._mint_(sender, amount)
    token.approve(noFlashLoanErc20, amount, {"from": sender})
    noFlash.deposit(amount, min_shares, {"from": sender})

    # withdraw
    shares = vault.balanceOf(sender)
    min_underlying = 1

    assert shares > 0

    vault.approve(noFlashLoanErc20, shares, {"from": sender})

    def snapshot():
        return {
            "token": {
                "sender": token.balanceOf(sender),
                "noFlash": token.balanceOf(noFlash),
                "vault": token.balanceOf(vault),
            },
            "vault": {
                "sender": vault.balanceOf(sender),
                "noFlash": vault.balanceOf(noFlash),
            },
            "noFlash": {"lastBlock": {"sender": noFlash.lastBlock(sender)}},
        }

    before = snapshot()
    tx = noFlash.withdraw(shares, min_underlying, {"from": sender})
    after = snapshot()

    # check token transfer
    assert after["token"]["sender"] == before["token"]["sender"] + amount
    assert after["token"]["noFlash"] == 0
    assert after["token"]["noFlash"] == before["token"]["noFlash"]
    assert after["token"]["vault"] == before["token"]["vault"] - amount

    # check shares transfer
    assert after["vault"]["sender"] < before["vault"]["sender"]
    assert after["vault"]["noFlash"] == 0
    assert after["vault"]["noFlash"] == before["vault"]["noFlash"]
    # check last block
    assert (
        after["noFlash"]["lastBlock"]["sender"]
        > before["noFlash"]["lastBlock"]["sender"]
    )
    assert after["noFlash"]["lastBlock"]["sender"] == tx.block_number


def test_withdraw_not_whitelist(accounts, noFlashLoanErc20, admin, token):
    amount = 100
    min_underlying = 1

    with brownie.reverts("!whitelist"):
        noFlashLoanErc20.withdraw(amount, min_underlying, {"from": accounts[1]})

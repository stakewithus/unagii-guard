import brownie


def test_deposit(accounts, noFlashLoanErc20, admin, token, erc20Vault):
    # rename fixtures
    noFlash = noFlashLoanErc20
    vault = erc20Vault

    amount = 100
    min_shares = 1
    sender = accounts[1]

    token._mint_(sender, amount)
    token.approve(noFlash, amount, {"from": sender})

    noFlash.setWhitelist(sender, True, {"from": admin})

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
    tx = noFlash.deposit(amount, min_shares, {"from": sender})
    after = snapshot()

    # check token transfer
    assert after["token"]["sender"] == before["token"]["sender"] - amount
    assert after["token"]["noFlash"] == 0
    assert after["token"]["noFlash"] == before["token"]["noFlash"]
    assert after["token"]["vault"] == before["token"]["vault"] + amount

    # check shares transfer
    assert after["vault"]["sender"] > before["vault"]["sender"]
    assert after["vault"]["noFlash"] == 0
    assert after["vault"]["noFlash"] == before["vault"]["noFlash"]
    # check last block
    assert (
        after["noFlash"]["lastBlock"]["sender"]
        > before["noFlash"]["lastBlock"]["sender"]
    )
    assert after["noFlash"]["lastBlock"]["sender"] == tx.block_number


def test_deposit_paused(accounts, noFlashLoanErc20, admin, token):
    noFlashLoanErc20.setPause(True, {"from": admin})

    amount = 100
    min_shares = 1

    with brownie.reverts("paused"):
        noFlashLoanErc20.deposit(amount, min_shares, {"from": accounts[1]})


def test_deposit_not_whitelist(accounts, noFlashLoanErc20, admin, token):
    amount = 100
    min_shares = 1

    with brownie.reverts("!whitelist"):
        noFlashLoanErc20.deposit(amount, min_shares, {"from": accounts[1]})


def test_deposit_min(accounts, noFlashLoanErc20, admin, token):
    amount = 100
    min_shares = 1000
    sender = accounts[1]

    token._mint_(sender, amount)
    token.approve(noFlashLoanErc20, amount, {"from": sender})

    noFlashLoanErc20.setWhitelist(sender, True, {"from": admin})

    with brownie.reverts("shares < min"):
        noFlashLoanErc20.deposit(amount, min_shares, {"from": accounts[1]})

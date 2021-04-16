# @version 0.2.11

from vyper.interfaces import ERC20

interface NoFlash:
    def vault() -> address: view
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

noFlash: address

@external
def __init__(_noFlash: address):
    self.noFlash = _noFlash

@external
def withdraw():
    vault: address = NoFlash(self.noFlash).vault()
    token: address = NoFlash(self.noFlash).token()

    shares: uint256 = ERC20(vault).balanceOf(self)
    assert shares > 0, "shares = 0"

    ERC20(vault).approve(self.noFlash, MAX_UINT256)
    NoFlash(self.noFlash).withdraw(shares, 1)

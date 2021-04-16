# @version 0.2.11

from vyper.interfaces import ERC20

interface Guard:
    def vault() -> address: view
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

guard: address

@external
def __init__(_guard: address):
    self.guard = _guard

@external
def withdraw():
    vault: address = Guard(self.guard).vault()
    token: address = Guard(self.guard).token()

    shares: uint256 = ERC20(vault).balanceOf(self)
    assert shares > 0, "shares = 0"

    ERC20(vault).approve(self.guard, MAX_UINT256)
    Guard(self.guard).withdraw(shares, 1)

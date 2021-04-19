# @version 0.2.11

from vyper.interfaces import ERC20

interface Guard:
    def vault() -> address: view
    def deposit(_min: uint256): payable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

guard: address
vault: address

@external
def __init__(_guard: address):
    self.guard = _guard
    self.vault = Guard(_guard).vault()

@external
@payable
def deposit(_min: uint256):
    Guard(self.guard).deposit(_min, value=msg.value)

    shares: uint256 = ERC20(self.vault).balanceOf(self)
    ERC20(self.vault).transfer(msg.sender, shares)

# @version 0.2.11

from vyper.interfaces import ERC20

interface Guard:
    def vault() -> address: view
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

guard: address
vault: address
token: address

@external
def __init__(_guard: address):
    self.guard = _guard
    self.vault = Guard(_guard).vault()
    self.token = Guard(_guard).token()

@external
def deposit(_amount: uint256, _min: uint256):
    ERC20(self.token).transferFrom(msg.sender, self, _amount)
    ERC20(self.token).approve(self.guard, _amount)
    Guard(self.guard).deposit(_amount, _min)

    shares: uint256 = ERC20(self.vault).balanceOf(self)
    ERC20(self.vault).transfer(msg.sender, shares)

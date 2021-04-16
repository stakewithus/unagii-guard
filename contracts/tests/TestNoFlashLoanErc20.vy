# @version 0.2.11

from vyper.interfaces import ERC20

interface NoFlashLoanErc20:
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

target: address

@external
def __init__(_noFlashLoanErc20: address):
    self.target = _noFlashLoanErc20

@external
def attack():
    token: address = NoFlashLoanErc20(self.target).token()

    bal: uint256 = ERC20(token).balanceOf(self)
    assert bal > 0, "bal = 0"

    ERC20(token).approve(self.target, MAX_UINT256)
    NoFlashLoanErc20(self.target).deposit(bal, 0)

    shares: uint256 = ERC20(self.target).balanceOf(self)
    NoFlashLoanErc20(self.target).withdraw(shares, 0)



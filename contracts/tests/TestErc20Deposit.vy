# @version 0.2.11

from vyper.interfaces import ERC20

interface Guard:
    def vault() -> address: view
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

interface TestWithdraw:
    def withdraw(): nonpayable

guard: address
testWithdraw: address

@external
def __init__(_guard: address, _testWithdraw: address):
    self.guard = _guard
    self.testWithdraw = _testWithdraw

@external
def deposit():
    """
    @dev Execute flash loan using different contracts for deposit and withdraw
    @dev Deposit `token`, transfer shares to `TestWithdraw`, call `withdraw`
    """
    vault: address = Guard(self.guard).vault()
    token: address = Guard(self.guard).token()

    bal: uint256 = ERC20(token).balanceOf(self)
    assert bal > 0, "bal = 0"

    ERC20(token).approve(self.guard, MAX_UINT256)
    Guard(self.guard).deposit(bal, 1)

    shares: uint256 = ERC20(vault).balanceOf(self)
    assert shares > 0, "shares = 0"

    ERC20(vault).transfer(self.testWithdraw, shares)
    TestWithdraw(self.testWithdraw).withdraw()

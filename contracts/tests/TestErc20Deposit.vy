# @version 0.2.11

from vyper.interfaces import ERC20

interface NoFlash:
    def vault() -> address: view
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

interface TestWithdraw:
    def withdraw(): nonpayable

noFlash: address
testWithdraw: address

@external
def __init__(_noFlash: address, _testWithdraw: address):
    self.noFlash = _noFlash
    self.testWithdraw = _testWithdraw

@external
def deposit():
    """
    @dev Execute flash loan using different contracts for deposit and withdraw
    @dev Deposit `token`, transfer shares to `TestWithdraw`, call `withdraw`
    """
    vault: address = NoFlash(self.noFlash).vault()
    token: address = NoFlash(self.noFlash).token()

    bal: uint256 = ERC20(token).balanceOf(self)
    assert bal > 0, "bal = 0"

    ERC20(token).approve(self.noFlash, MAX_UINT256)
    NoFlash(self.noFlash).deposit(bal, 1)

    shares: uint256 = ERC20(vault).balanceOf(self)
    assert shares > 0, "shares = 0"

    ERC20(vault).transfer(self.testWithdraw, shares)
    TestWithdraw(self.testWithdraw).withdraw()

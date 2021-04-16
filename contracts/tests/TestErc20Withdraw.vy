# @version 0.2.11

from vyper.interfaces import ERC20

interface Guard:
    def vault() -> address: view
    def token() -> address: view
    def deposit(_amount: uint256, _min: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

interface TestDeposit:
    def deposit(_amount: uint256, _min: uint256): nonpayable

guard: address
vault: address
token: address
testDeposit: address

@external
def __init__(_guard: address, _testDeposit: address):
    self.guard = _guard
    self.vault = Guard(_guard).vault()
    self.token = Guard(_guard).token()
    self.testDeposit = _testDeposit

@external
def withdraw(_shares: uint256, _min: uint256):
    ERC20(self.vault).transferFrom(msg.sender, self, _shares)
    ERC20(self.vault).approve(self.guard, _shares)
    Guard(self.guard).withdraw(_shares, _min)

    bal: uint256 = ERC20(self.token).balanceOf(self)
    ERC20(self.token).transfer(msg.sender, bal)

@external
def attack():
    """
    @dev Execute flash loan using different contracts for deposit and withdraw
    @dev Deposit `token`, transfer shares to `TestWithdraw`, call `withdraw`
    """
    bal: uint256 = ERC20(self.token).balanceOf(self)
    assert bal > 0, "bal = 0"

    ERC20(self.token).approve(self.testDeposit, bal)
    TestDeposit(self.testDeposit).deposit(bal, 1)

    shares: uint256 = ERC20(self.vault).balanceOf(self)
    assert shares > 0, "shares = 0"

    ERC20(self.vault).approve(self.guard, MAX_UINT256)
    Guard(self.guard).withdraw(shares, 1)

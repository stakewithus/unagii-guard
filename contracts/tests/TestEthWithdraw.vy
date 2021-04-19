# @version 0.2.11

from vyper.interfaces import ERC20

interface Guard:
    def vault() -> address: view
    def deposit(_min: uint256): payable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

interface TestDeposit:
    def deposit( _min: uint256): payable

guard: address
vault: address
testDeposit: address

@external
def __init__(_guard: address, _testDeposit: address):
    self.guard = _guard
    self.vault = Guard(_guard).vault()
    self.testDeposit = _testDeposit

@external
@payable
def __default__():
    pass

@external
def withdraw(_shares: uint256, _min: uint256):
    ERC20(self.vault).transferFrom(msg.sender, self, _shares)
    ERC20(self.vault).approve(self.guard, _shares)
    Guard(self.guard).withdraw(_shares, _min)

    raw_call(msg.sender, b"", value=self.balance)

@external
def attack():
    """
    @dev Execute flash loan using different contracts for deposit and withdraw
    @dev Deposit `token`, transfer shares to `TestWithdraw`, call `withdraw`
    """
    bal: uint256 = self.balance
    assert bal > 0, "bal = 0"

    TestDeposit(self.testDeposit).deposit(1, value=bal)

    shares: uint256 = ERC20(self.vault).balanceOf(self)
    assert shares > 0, "shares = 0"

    ERC20(self.vault).approve(self.guard, MAX_UINT256)
    Guard(self.guard).withdraw(shares, 1)

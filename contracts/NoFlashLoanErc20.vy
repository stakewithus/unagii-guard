# @version ^0.2.11

from vyper.interfaces import ERC20 

# TODO: license
# TODO: comments

interface Erc20Vault:
    def token() -> address: view
    def deposit(_amount: uint256): nonpayable
    def withdraw(_shares: uint256, _min: uint256): nonpayable

event SetPause:
    paused: bool

event SetWhitelist:
    addr: indexed(address)
    approved: bool

event Deposit:
    sender: indexed(address)
    amount: uint256

event Withdraw:
    sender: indexed(address)
    amount: uint256

admin: public(address)
nextAdmin: public(address)
paused: public(bool)
vault: public(address)
token: public(address)
whitelist: public(HashMap[address, bool])

lastBlock: public(HashMap[address, uint256])

@external
def __init__(_vault: address):
    assert _vault != ZERO_ADDRESS, "vault = 0 address"
    self.admin = msg.sender

    self.vault = _vault
    self.token = Erc20Vault(_vault).token()

    # TODO: safe transfer, safe approve
    # deposit
    ERC20(self.token).approve(self.vault, MAX_UINT256)
    # withdraw
    ERC20(self.vault).approve(self.vault, MAX_UINT256)

@external
def setNextAdmin(_nextAdmin: address):
    assert msg.sender == self.admin, "!admin"
    # allow next admin = zero address
    self.nextAdmin = _nextAdmin

@external
def claimAdmin():
    assert msg.sender == self.nextAdmin, "!next admin"
    self.admin = msg.sender
    self.nextAdmin = ZERO_ADDRESS

@external
def setPause(_paused: bool):
    assert msg.sender == self.admin, "!admin"
    self.paused = _paused
    log SetPause(_paused)

@external
def setWhitelist(_addr: address, _approved: bool):
    assert msg.sender == self.admin, "!admin"
    self.whitelist[_addr] = _approved
    log SetWhitelist(_addr, _approved)

@nonreentrant("lock")
@external
def deposit(_amount: uint256, _min: uint256):
    assert not self.paused, "paused"
    assert self.whitelist[msg.sender], "!whitelist"

    # TODO: integration test
    assert block.number > self.lastBlock[tx.origin], "no flash"
    # track EOA
    # tracking EOA prevents the following flash loan
    # 1. contract A calls deposit
    # 2. contract A transfers shares to contract B
    # 3. contract B calls withdraw
    self.lastBlock[tx.origin] = block.number
    
    ERC20(self.token).transferFrom(msg.sender, self, _amount)

    # cache, saves about 2000 gas
    _vault: address = self.vault

    sharesBefore: uint256 = ERC20(_vault).balanceOf(self)
    # if token has fee on transfer, this function will fail
    Erc20Vault(_vault).deposit(_amount)
    sharesAfter: uint256 = ERC20(_vault).balanceOf(self)

    sharesDiff: uint256 = sharesAfter - sharesBefore

    assert sharesDiff >= _min, "shares < min"

    ERC20(_vault).transfer(msg.sender, sharesDiff)

    log Deposit(msg.sender, _amount)

@nonreentrant("lock")
@external
def withdraw(_shares: uint256, _min: uint256):
    # allow withdraw even if paused = true
    assert self.whitelist[msg.sender], "!whitelist"

    assert block.number > self.lastBlock[tx.origin], "no flash"
    # track EOA
    self.lastBlock[tx.origin] = block.number

    # cache, saves about 1000 gas
    _vault: address = self.vault
    _token: address = self.token

    ERC20(_vault).transferFrom(msg.sender, self, _shares)

    balBefore: uint256 = ERC20(_token).balanceOf(self)
    Erc20Vault(_vault).withdraw(_shares, _min)
    balAfter: uint256 = ERC20(_token).balanceOf(self)

    diff: uint256 = balAfter - balBefore

    ERC20(_token).transfer(msg.sender, diff)

    log Withdraw(msg.sender, diff)

@external
def sweep(_token: address):
    assert msg.sender == self.admin, "!admin"
    bal: uint256 = ERC20(_token).balanceOf(self)
    ERC20(_token).transfer(self.admin, bal)


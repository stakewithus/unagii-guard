# @version 0.2.11

from vyper.interfaces import ERC20

ETH: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE

token: public(address)
balanceOf: public(HashMap[address, uint256])

@external
def __init__():
    self.token = ETH

# allow ETH for testing
@external
def __default__():
    pass

@external
@payable
def deposit():
    self.balanceOf[msg.sender] += msg.value

@external
def withdraw(_shares: uint256, _min: uint256):
    self.balanceOf[msg.sender] -= _shares
    raw_call(msg.sender, b"", value=_shares)

@external
def transfer(_to: address, _shares: uint256) -> bool:
    self.balanceOf[msg.sender] -= _shares
    self.balanceOf[_to] += _shares
    return True

@external
def transferFrom(_from: address, _to: address, _shares: uint256) -> bool:
    self.balanceOf[_from] -= _shares
    self.balanceOf[_to] += _shares
    return True

@external
def approve(_spender: address, _amount: uint256) -> bool:
    return True

# used for mainnet test
@external
def setWhitelist(_addr: address, _approved: bool):
    pass
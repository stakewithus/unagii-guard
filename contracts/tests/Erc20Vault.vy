# @version 0.2.11

from vyper.interfaces import ERC20

token: public(address)
balanceOf: public(HashMap[address, uint256])

@external
def __init__(_token: address):
    self.token = _token

@external
def deposit(_amount: uint256):
    ERC20(self.token).transferFrom(msg.sender, self, _amount)
    self.balanceOf[msg.sender] += _amount

@external
def withdraw(_shares: uint256, _min: uint256):
    self.balanceOf[msg.sender] -= _shares
    ERC20(self.token).transfer(msg.sender, _shares)

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
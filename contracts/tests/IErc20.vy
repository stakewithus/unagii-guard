# @version 0.2.11

"""
IErc20 used for mainnet test
"""

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256

event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256


name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
balanceOf: public(HashMap[address, uint256])
allowances: HashMap[address, HashMap[address, uint256]]

@external
@view
def totalSupply() -> uint256:
    return 0


@external
@view
def allowance(_owner : address, _spender : address) -> uint256:
    return 0


@external
def transfer(_to : address, _value : uint256) -> bool:
    return True


@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    return True


@external
def approve(_spender : address, _value : uint256) -> bool:
    return True
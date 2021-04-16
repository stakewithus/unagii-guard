# @version 0.2.11

deposited: public(HashMap[address, uint256])

@external
@payable
def deposit_for(_receiver: address) -> bool:
    self.deposited[_receiver] += msg.value
    return True

@external
def withdraw_from(_value: uint256) -> bool:
    assert self.deposited[msg.sender] >= _value, "Insufficient balance"
    self.deposited[msg.sender] = _value
    send(msg.sender, _value)
    return True
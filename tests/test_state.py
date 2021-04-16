import brownie
from brownie.test import strategy

class StateMachine:

    value = strategy('uint256', max_value="1 ether")
    address = strategy('address')

    def __init__(cls, accounts, Depositer):
        # deploy the contract at the start of the test
        cls.accounts = accounts
        cls.contract = Depositer.deploy({'from': accounts[0]})

    def setup(self):
        # zero the deposit amounts at the start of each test run
        self.deposits = {i: 0 for i in self.accounts}

    def rule_deposit(self, address, value):
        # make a deposit and adjust the local record
        self.contract.deposit_for(address, {'from': self.accounts[0], 'value': value})
        self.deposits[address] += value

    def rule_withdraw(self, address, value):
        if self.deposits[address] >= value:
            # make a withdrawal and adjust the local record
            self.contract.withdraw_from(value, {'from': address})
            self.deposits[address] -= value
        else:
            # attempting to withdraw beyond your balance should revert
            with brownie.reverts("Insufficient balance"):
                self.contract.withdraw_from(value, {'from': address})

    def invariant(self):
        # compare the contract deposit amounts with the local record
        for address, amount in self.deposits.items():
            assert self.contract.deposited(address) == amount


def test_stateful(Depositer, accounts, state_machine):
    state_machine(StateMachine, accounts, Depositer)
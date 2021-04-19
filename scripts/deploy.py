from brownie import GuardErc20, GuardEth, accounts, network

CONFIG = {
    "ropsten": {
        "erc20_vault": "0x83698950B13d0B8B1eAF37D6f0f584E6D71D4964",
        "eth_vault": "0x2405927Cfa0087C53593A9D97FEE8BcADDc6A008",
    },
    "mainnet": {
        "dev_usdc_vault": "0x167E3254a9298ebF29F67e0AE0326d2018c9bC44",
        "dev_eth_vault": "0x72E357f7635163493F153A0Bd3F03C15C14A51C6",
    },
}


def deploy_ropsten_erc20():
    print("ERC20 Vault")

    vault = CONFIG["ropsten"]["erc20_vault"]
    deploy("ropsten", GuardErc20, vault)


def deploy_ropsten_eth():
    print("ETH Vault")

    vault = CONFIG["ropsten"]["eth_vault"]
    deploy("ropsten", GuardEth, vault)


def deploy_dev_usdc():
    print("dev USDC Vault")

    vault = CONFIG["mainnet"]["dev_usdc_vault"]
    deploy("mainnet", GuardErc20, vault)


def deploy_dev_eth():
    print("dev ETH Vault")

    vault = CONFIG["mainnet"]["dev_eth_vault"]
    deploy("mainnet", GuardEth, vault)


def deploy(network_name, Guard, vault):
    assert network_name == network.show_active()
    print("Network:", network_name)

    account = accounts.load("dev")
    bal = account.balance()
    print("Account:", account)
    print("ETH balance:", bal)
    print("-------------------")
    print("Vault:", vault)

    Guard.deploy(vault, {"from": account})


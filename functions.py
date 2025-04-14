import re
import requests
from web3 import Web3

## IS THE FORMAT VALID

# 1. Check address format: starts with 0x and 40 hex chars
def is_valid_format(ca):
    return re.fullmatch(r"0x[a-fA-F0-9]{40}", ca) is not None

# 2. Check if checksum is valid (optional, but useful)
def is_checksum_address(ca):
    return Web3.isChecksumAddress(ca)

# 3. Full validation (checksum optional)
def is_valid_bsc_contract_address(ca, require_checksum=False):
    if not is_valid_format(ca):
        return False
    if require_checksum:
        return is_checksum_address(ca)
    return True
       

## IS IT A TOKEN ON BSC
def is_token_contract(ca, api_key):
    url = "https://api.bscscan.com/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": ca,
        "apikey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "1":
        print("Error or unverified contract.")
        return False

    source_code = data["result"][0].get("SourceCode", "")
    contract_name = data["result"][0].get("ContractName", "")

    # Simple keyword check for ERC20/BEP20 interface
    is_token = any(keyword in source_code for keyword in ["ERC20", "BEP20", "totalSupply", "balanceOf", "transfer"])
    
    return is_token


def token_data(ca: str):
    
    url = f"https://api.dexscreener.com/latest/dex/search/?q={ca}"
    
    response = requests.get(url)
    data = response.json()
    
    # DexScreener returns a list of pairs (you can select the first or filter by base token)
    if not data.get("pairs"):
        response = "No trading pair found for this token."

    else:

        pair = data["pairs"][0]  # You can improve this by choosing the highest liquidity pool

        metrics = {
            "token_name": pair.get("baseToken", {}).get("name"),
            "symbol": pair.get("baseToken", {}).get("symbol"),
            "price_usd": float(pair.get("priceUsd", 0)),
            "market_cap_usd": float(pair.get("fdv", 0)),  # FDV = Fully Diluted Valuation
            "liquidity_usd": float(pair.get("liquidity", {}).get("usd", 0)),
            "dex": pair.get("dexId"),
            "pair_url": pair.get("url")
        }
  
        response = f"""
CA: {ca}
Token Name: {metrics["token_name"]}
Symbol: {metrics["symbol"]}
Price: ${metrics["price_usd"]}
Market Cap: ${metrics["market_cap_usd"]}
Liquidity: ${metrics["liquidity_usd"]}
DEX: {metrics["dex"]}\n
https://dexscreener.com/bsc/{ca}
        """

    return response
import requests
import json
import os
import dotenv
dotenv.load_dotenv()
X_CMC_PRO_API_KEY = os.getenv("X_CMC_PRO_API_KEY")

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': X_CMC_PRO_API_KEY,
}

def fetch_api(tokenName, intent):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
    params = {
    'limit':'5000',
    'convert': "USD"
    }
    newData = []
    response = requests.get(url, headers=headers, params=params)
    results = response.json().get("data", [])

    for result in results:
        symbol = result["symbol"]
        price = result["quote"]["USD"]["price"]
        marketCap = result["quote"]["USD"]["market_cap"]
        volume = result["quote"]["USD"]["volume_24h"]
        fullName = result["name"]
        totalSupply = result["total_supply"]
        newData.append({
            "Symbol": symbol, 
            "Price" : price, 
            "Volume" : volume, 
            "Capitalization": marketCap, 
            "TotalSupply": totalSupply, 
            "Fullname": fullName})

    with open('data.json', 'w') as file:
        json.dump(newData, file)
    if tokenName:
        try:
            with open('data.json', 'r') as file:
                results = json.load(file)
                for result in results:
                    if result["Symbol"] == tokenName or result["Fullname"] == tokenName.title():
                        return result[intent]
        except Exception as e:
            print(e)

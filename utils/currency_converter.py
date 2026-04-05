import requests

def currency_converter(amount, from_currency, to_currency):
    url = "https://api.frankfurter.dev"
    query = {
        "base": from_currency,
        "quotes": to_currency,
    }
    response = requests.get(url=url+"/v2/rates", params=query)
    if response.status_code != 200:
        return None
    try:
        rate = response.json()[0]['rate']
        return amount * rate
    except KeyError:
        return None

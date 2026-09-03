# https://api.frankfurter.dev/v1/latest?base=USD

import requests


def get_currency_rate(base: str) -> dict:
    url = f"https://api.frankfurter.dev/v1/latest?base={base}"
    response = requests.get(url)
    data = response.json()
    return data["rates"]
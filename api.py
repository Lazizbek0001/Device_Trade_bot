import requests
api_key = '7a2804ea5299bfc51767dfa0'


def exchange(currency):
    url = f' https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/{currency}'
    req = requests.get(url)
    data = req.json()
    res = str(data['conversion_rate'])[:8]
    return res








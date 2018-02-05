# Binance Trader v0.1
import sys, os, base64, datetime, hashlib, hmac
import json
import requests


# urls
base_url = "https://api.binance.com"
headers = { "X-MBX-APIKEY": "Abcd132464684948"}


def get_server_time():
    url = base_url + "/api/v1/exchangeInfo"
    res = requests.get(url)
    return res.json()


def get_exchange_info():
    url = base_url + "/api/v1/exchangeInfo"
    res = requests.get(url)
    return res.json()


def get_depth():
    """get the later asks and bids (bid lower than asking?)"""
    url = base_url + "/api/v1/depth"
    res = requests.get(url, params={ "symbol": "ETHUSDT", "limit": "5" })
    return res.json()

# TRADE
#
def test_order():
    """sends a test order - does not send it to the matching machine"""
    url = base_url + "/api/v3/order/test"

    """
    params:
    symbol      ETHUSDT
    side        SELL        # operation
    type        LIMIT
    timeInForce GTC         # timezone
    quantity    1
    price       0.1         # how do you set this one?
    recvWindow  5000        # time window
    timestamp   9684948198
    """

    """
    STEP-1: get a signature using the query string:
    ======================================================
    query_string = "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559" 
    secret_key = "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
    echo -n query_string | openssl dgst -sha256 -hmac secret_key 
    signature => c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71

    STEP-2: Send the POST request
    ======================================================
    endpoint: 'https://api.binance.com/api/v3/order'
    method:   'POST'
    headers:  { "X-MBX-APIKEY": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A" }

    payload:  {
        symbol=LTCBTC
        side=BUY
        type=LIMIT
        timeInForce=GTC
        quantity=1
        price=0.1
        recvWindow=6000000
        timestamp=1499827319559
        signature=c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71'
    """

    """
    # signed params
    # signature
    # secretKey as the key
    # totalParams
    # timestamp
    # recvWindow
    """

    request = requests.Request(
        'POST', 'https://poloniex.com/tradingApi',
        data=payload, headers=headers)

    prepped = request.prepare()
    signature = hmac.new(secret, prepped.body, digestmod=hashlib.sha512)
    prepped.headers['Sign'] = signature.hexdigest()

    with requests.Session() as session:
        response = session.send(prepped)
        print(response)


print(json.dumps(get_depth(), sort_keys=True, indent=4))


import hashlib
import hmac
import urllib.parse
import requests
# from freekassa import FreeKassaApi

from fe_bot.settings import FREEKASSA_FIRST_SECRET_KEY, FREEKASSA_SECOND_SECRET_KEY, \
    FREEKASSA_MERCHANT_ID, FREEKASSA_WALLET_ID, FREEKASSA_API_KEY


class FreeKassaApi:
    BASE_URL = "https://api.freekassa.ru/v1"
    BASE_URL_SCI = "https://pay.freekassa.ru/"
    CREATE_ORDER_PATH = "/orders/create"

    def __init__(self, api_key: str, first_secret_key: str, second_secret_key: str,
                 merchant_id: int, wallet_id: int):
        self.api_key = api_key
        self.first_secret_key = first_secret_key
        self.second_secret_key = second_secret_key
        self.merchant_id = merchant_id
        self.wallet_id = wallet_id

    def create_signature(self, data: dict) -> str:
        sorted_dict = dict(((key, data[key]) for key in sorted(data)))
        raw_values = ""
        for value in sorted_dict.values():
            raw_values += f"{value}|"
        raw_values = raw_values[0:-1:]
        print(raw_values)
        digest = hmac.new(self.api_key.encode(), raw_values.encode(), hashlib.sha256)
        return digest.hexdigest()

    def create_sci_signature(self, order_id: str, amount: float, currency: str) -> str:
        raw_values = f"{self.merchant_id}:{amount}:{self.first_secret_key}:{currency}:{order_id}"
        digest = hashlib.md5(raw_values.encode())
        return digest.hexdigest()

    def create_order(self, nonce: int, paymentId: int, email: str,
                     ip: str, amount: float, i: int = 6, currency: str = "RUB"):
        payload = {"shopId": self.merchant_id, "nonce": nonce, "paymentId": paymentId, "i": i, "email": email, "ip": ip,
                   "amount": amount, "currency": currency}
        payload["signature"] = self.create_signature(payload)
        print(payload)
        url = self.BASE_URL + self.CREATE_ORDER_PATH + f"?shopId={self.merchant_id}"
        return requests.post(url, json=payload)

    def create_sci(self, oa: float, o: str, currency: str = "RUB"):

        params = {"m": self.merchant_id, "oa": oa, "o": o, "currency": currency,
                  "s": self.create_sci_signature(o, oa, currency)}
        return self.BASE_URL_SCI + "?" + urllib.parse.urlencode(params)


freekassa_client = FreeKassaApi(
    api_key=FREEKASSA_API_KEY,
    first_secret_key=FREEKASSA_FIRST_SECRET_KEY,
    second_secret_key=FREEKASSA_SECOND_SECRET_KEY,
    merchant_id=FREEKASSA_MERCHANT_ID,
    wallet_id=FREEKASSA_WALLET_ID)

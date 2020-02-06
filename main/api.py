import requests
from requests.auth import HTTPBasicAuth


def get_data(word):
    data = requests.get(f"https://dictapi.lexicala.com/search?source=global&language=en&text={word}&morph=true",
                        auth=HTTPBasicAuth('namangala', 'ilovecoding1@'))
    return data.json()


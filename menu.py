from TwitterAPI import TwitterAPI
from key import API_key,API_secret_key,secret_token,token
from requests import get
from scrapy import Selector

api = TwitterAPI(API_key,API_secret_key,token,secret_token)
URL = "https://www.crous-orleans-tours.fr/restaurant/cafeteria-lahitolle/"
url = "https://fr.wikipedia.org/wiki/Star_Wars"

def PostMessage(message):
    reponse = api.request('statuses/update', {'status':message})
    return True if reponse.status_code == 200  else False


def getPage(URL,source):
    reponse = get(URL)
    if reponse.status_code == 200:
        source=reponse.text
        return True
    return False






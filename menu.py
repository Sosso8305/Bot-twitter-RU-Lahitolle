from TwitterAPI import TwitterAPI
from key import API_key,API_secret_key,secret_token,token
from requests import get
import pandas as pd
from bs4 import BeautifulSoup
import csv



class MenuRuOnTwitter():
    def __init__(self,API_key,API_secret_key,token,secret_token,URL):
        self.api = TwitterAPI(API_key,API_secret_key,token,secret_token)
        self.URL=URL        
        

    def PostMessage(self,message):
        if(len(message)<140):
            reponse = self.api.request('statuses/update', {'status':message})
            return True if reponse.status_code == 200  else False
        return False


    def getPage(self,URL):
        reponse = get(URL)
        if reponse.status_code == 200:
            self.source=reponse.text
            return True
        return False



    def Research(self):
        if(self.getPage(self.URL)):
            self.data=[]
            
            HtmlParser = BeautifulSoup(self.source, 'html.parser')
            listToday=HtmlParser.find('ul',attrs={'class':'slides'})
            self.Today=listToday.find('h3').getText()
            listMenu = listToday.find('div',attrs={'class':'content clearfix'})
            listRepas = listMenu.find_all('ul',attrs={'class':'liste-plats'})



            for Repas in listRepas:
                tuple_data=Repas.find_all('li')
                for i in range(len(tuple_data)):
                    if( len(tuple_data[i].getText()) != 0):
                        self.data.append(tuple_data[i].getText())

            
        else:
            print("erreur: getPage()")


URL = "https://www.crous-orleans-tours.fr/restaurant/cafeteria-lahitolle/"
Bot = MenuRuOnTwitter(API_key,API_secret_key,token,secret_token,URL)

Bot.Research()


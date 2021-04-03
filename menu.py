from TwitterAPI import TwitterAPI
from key import API_key,API_secret_key,secret_token,token
from requests import get
from bs4 import BeautifulSoup
from datetime import date



DATE="Menu du vendredi 2 avril 2021"

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

    def DateOfToday(self):
        days=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
        months=['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
        Date=date.today()
        day=days[Date.weekday()]
        month=months[Date.month-1]
        MessageDate= "Menu du "+ day +" "+ str(Date.day) + " "+month+ " " + str(Date.year)

        return MessageDate

    def Research(self):
        if(self.getPage(self.URL)):
            self.data=[]
            
            HtmlParser = BeautifulSoup(self.source, 'html.parser')
            listToday=HtmlParser.find('ul',attrs={'class':'slides'})

            #print(listToday)
            
            indice=0
            find=False

            listTodays=listToday.find_all('h3')
            for day in listTodays:
                if(day.getText() == DATE): # self.DateOfToday()):
                    find = True
                    break

                indice += 1

            if(find):
                listMenu=listToday.find_all('div',attrs={'class':'content clearfix'})[indice]
                listRepas = listMenu.find_all('ul',attrs={'class':'liste-plats'})

                for Repas in listRepas:
                    tuple_data=Repas.find_all('li')
                    for i in range(len(tuple_data)):
                        if( len(tuple_data[i].getText()) != 0):
                            self.data.append(tuple_data[i].getText())

                return True

            else:
                print(self.DateOfToday()+" don't exits")
                return False
        
            
        else:
            print("erreur: getPage()")
            return False

    def SortData(self):
        midi=[]
        soir=[]
        for menu in self.data:
            if(menu[:4] == "MIDI"):
                midi.append(menu[7:])
            else:
                soir.append(menu[7:])
        
        MENU = f" \033[4m{self.DateOfToday()}\033[0m   \n\n  MIDI \n \t Entrée --> {midi[0]}  \n \t Plat --> {midi[1]}  \n \t Plat Végétarien--> {midi[2]}  \n \t Désert--> {midi[3]} \n\n Soir  \n \t Entrée --> {soir[0]} \n \t Plat --> {soir[1]} \n \t Désert --> {soir[2]}"
        

        return MENU 





URL = "https://www.crous-orleans-tours.fr/restaurant/cafeteria-lahitolle/"
Bot = MenuRuOnTwitter(API_key,API_secret_key,token,secret_token,URL)







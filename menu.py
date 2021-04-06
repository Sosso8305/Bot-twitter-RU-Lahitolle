from TwitterAPI import TwitterAPI
from key import API_key,API_secret_key,secret_token,token
from requests import get
from bs4 import BeautifulSoup
from datetime import date



DEBUG=0

class MenuRuOnTwitter():
    def __init__(self,API_key,API_secret_key,token,secret_token,URL):
        self.api = TwitterAPI(API_key,API_secret_key,token,secret_token)
        self.URL=URL        
        

    def PostMessage(self,message):
        if(len(message)<281):
            reponse = self.api.request('statuses/update', {'status':message})
            return True if reponse.status_code == 200  else False
        return False


    def getPage(self):
        reponse = get(self.URL)
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
        if(self.getPage()):
            self.data=[]
            
            HtmlParser = BeautifulSoup(self.source, 'html.parser')
            listToday=HtmlParser.find('ul',attrs={'class':'slides'})

            
            indice=0
            find=False

            listTodays=listToday.find_all('h3')
            for day in listTodays:
                if(day.getText() == self.DateOfToday()):
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
                if(DEBUG):
                    print(self.DateOfToday()+" don't exits")
                return False
        
            
        else:
            if(DEBUG):
                print("erreur: getPage()")
            return False

    def SortData(self):
        midi=[]
        soir=[]
        for menu in self.data:
            if(menu[:4] == "MIDI"):
                midi.append(menu[6:])
            else:
                soir.append(menu[6:])
        
        MENU = [f"🍴{self.DateOfToday()}\n\n🌞Midi:\n\n🥬Entrée-->{midi[0]}\n🍗Plat-->{midi[1]}\n🥦Plat Végétarien-->{midi[2]}\n🍩Dessert-->{midi[3]}",f"🍴{self.DateOfToday()}\n\n🌝Soir:\n\n🥬Entrée-->{soir[0]}\n🍗Plat -->{soir[1]}\n🍩Désert-->{soir[2]}"]
        

        return MENU 

    def Tweet(self):
        if(self.Research()):
            menu = self.SortData()
            if(not(self.PostMessage(menu[0]) and self.PostMessage(menu[1]))):
                self.PostMessage(f"🍴{self.DateOfToday()} \n\n 🔔 Un des menus est trop long pour Twitter 🔔  \n Donc GO sur le site du RU ... \n\n 🌐 {self.URL}")
        else:
            nothing = f"🍴{self.DateOfToday()}  \n\n ⚠️Il n'y a pas de menu pour aujourd'hui⚠️"
            return self.PostMessage(nothing)





URL = "https://www.crous-orleans-tours.fr/restaurant/cafeteria-lahitolle/"
Bot = MenuRuOnTwitter(API_key,API_secret_key,token,secret_token,URL)

Bot.Tweet()







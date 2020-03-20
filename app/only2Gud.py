from bs4 import BeautifulSoup
import requests

def productGud(string):
    return "%20".join(string.split())

class TwoGud():
    def __init__(self,product):
        self.__product = product
        self._request='https://www.2gud.com/search?q='+productGud(product)
        twogudRespond = requests.post('https://www.2gud.com/search?q='+productGud(product)).text
        soup = BeautifulSoup(twogudRespond, 'lxml')
        self.__soup = soup
    
    def get_first_price(self):
        try:
            strPrice = self.__soup.find('div', class_='_1vC4OE').text[1:]
            name = self.__soup.find('div', class_='_3wU53n').text
            price = int(''.join(strPrice.split(',')))  
            print("Worked")
            return {"price":price,"name":name,"website":self._request}
        except:
            return []

    def get_first_delivery(self):
        return []

    def get_first_price_and_delivery(self):
        try:
            strPrice = self.__soup.find('div', class_='_1vC4OE').text[1:]
            delivery = '-'
            price = int(''.join(strPrice.split(',')))  
            return {"price":price,"delivery":delivery,"website":self._request}
        except:
            return []

    def get_first_n_complete(self, n):
        b = 1
        gudListName = []
        gudListPrice = []
        gudListImage =[]
        gudListURL =[]
        title = self.__soup.find_all('div', class_='_3wU53n')
        for i in range(min(n,len(title))):
            gudListName.append(title[i].text)
        for price in self.__soup.find_all('div', class_='_1vC4OE'):
            try:
                k = price.text
                am = int(''.join(k[1:].split(',')))
                gudListPrice.append(am)
            except:
                gudListPrice.append('None')
            b += 1
            if b>n:
                break
        images = self.__soup.find_all('img', class_='_1Nyybr')
        for i in range(min(n, len(images))):
            try:
                gudListImage.append(images[i]["src"])
            except:
                gudListImage.append('None')
        URL = self.__soup.find_all('a', class_='_31qSD5')
        for i in range(min(n, len(URL))):
            try:
                gudListURL.append(str('https://www.2gud.com') + str(URL[i]['href']))
            except:
                gudListURL.append('None')
        dictTwogud = []
        for m in range(len(gudListName)):
            dictTwogud.append(
                {
                    "name":gudListName[m],
                    "price":gudListPrice[m],
                    "image":gudListImage[m],
                    "url":gudListURL[m]
                }
            )
        return dictTwogud
if __name__=="__main__":
    userInput = input('Enter The Name of Product >>> ')
    obj = TwoGud(userInput)
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(6))
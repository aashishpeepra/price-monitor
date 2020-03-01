from bs4 import BeautifulSoup
import requests

def productPaytm(string):
    return "%20".join(string.split())

class Paytm():
    def __init__(self,product):
        self.__product = product
        self._request='https://paytmmall.com/shop/search?&q='+productPaytm(product)
        print(self._request)
        ptmRespond = requests.get('https://paytmmall.com/shop/search?&q='+productPaytm(product)).text
        soup = BeautifulSoup(ptmRespond, 'lxml')
        self.__soup = soup
        # print(len(ptmRespond))
        # print(ptmRespond)

    def get_first_price(self):
        try:
            strObj = self.__soup.find('div', class_='_1kMS').span.text
            price = int(''.join(strObj.split(',')))
            name = self.__soup.find('div', class_='UGUy').text
            return {"price":price,"name":name,"website":self._request}
        except:
            return []
    
    def get_first_delivery(self):
        return []

    def get_first_price_and_delivery(self):
        try:
            strObj = self.__soup.find('div', class_='_1kMS').span.text
            price = int(''.join(strObj.split(',')))
            delivery = '-'
            return {"price":price,"delivery":delivery,"website":self._request}
        except:
            return []

    def get_first_n_complete(self, n):
        b = 1
        d = 1
        ptmListName = []
        ptmListPrice = []
        ptmListImage =[]
        ptmListURL =[]
        title = self.__soup.find_all('div', class_='UGUy')
        for i in range(min(n, len(title))):
            ptmListName.append(title[i].text)
        for price in self.__soup.find_all('div', class_='_1kMS'):
            try:
                k = price.span.text
                price = int(''.join(k.split(',')))
                ptmListPrice.append(price)
            except:
                ptmListPrice.append('None')
            b += 1
            if b>n:
                break
        images = self.__soup.find_all('div', class_='_3nWP')
        for i in range(min(n, len(images))):
            try:
                k = images[i].img['src']
                ptmListImage.append(k)
            except:
                ptmListImage.append('None')
        for URL in self.__soup.find_all('a', class_='_8vVO'):
            try:
                ptmListURL.append(str('https://paytmmall.com/') + str(URL['href']))
            except:
                ptmListURL.append('None')
            d += 1
            if d>n:
                break

        dictPaytm = []
        for m in range(len(ptmListName)):
            dictPaytm.append(
                {
                    "name":ptmListName[m],
                    "price":ptmListPrice[m],
                    "image":ptmListImage[m],
                    "url":ptmListURL[m]
                }
            )
        return dictPaytm
if __name__=="__main__":
    userInput = input('Enter The Name of Product >>> ')
    obj1 = Paytm(userInput)
    print(obj1.get_first_price())
    print(obj1.get_first_delivery())
    print(obj1.get_first_price_and_delivery())
    print(obj1.get_first_n_complete(6))
from bs4 import BeautifulSoup
import requests

def productGrofers(string):
    return "+".join(string.split())

class Grofers():
    def __init__(self,product):
        self.__product = product
        self.__request='https://grofers.com/s/?q='+productGrofers(product)
        grfRespond = requests.post('https://grofers.com/s/?q='+productGrofers(product)).text
        soup = BeautifulSoup(grfRespond, 'lxml')
        self.__soup = soup
    
    def get_first_price(self):
        try:
            strPrice = self.__soup.find('span', class_='plp-product__price--new').text[1:]
            price = int(''.join(strPrice.split(',')))  
            return {"price":price,"website":self.__request}
        except:
            return []

    def get_first_delivery(self):
        return []

    def get_first_price_and_delivery(self):
        try:
            strPrice = self.__soup.find('span', class_='plp-product__price--new').text[1:]
            price = int(''.join(strPrice.split(',')))
            delivery = '-'
            return {"price":price,"delivery":delivery,"website":self.__request}
        except:
            return []

    def get_first_n_complete(self, n):
        b = 1
        grfListName = []
        grfListPrice = []
        grfListURL =[]
        title = self.__soup.find_all('div', class_='plp-product__name--box')
        for i in range(min(n,len(title))):
            grfListName.append(title[i].text)
        for price in self.__soup.find_all('span', class_='plp-product__price--new'):
            try:
                k = price.text
                am = int(''.join(k[1:].split(',')))
                grfListPrice.append(am)
            except:
                grfListPrice.append('None')
            b += 1
            if b>n:
                break
        for URL in self.__soup.find_all('a', class_='product__wrapper'):
            try:
                k = URL['href']
                grfListURL.append(str('https:/grofers.com/')+str(k))
            except:
                grfListURL.append('None')
        dictGrofers = []
        for m in range(len(grfListPrice)):
            dictGrofers.append(
                {
                    "name":grfListName[m],
                    "price":grfListPrice[m],
                    "url":grfListURL[m]
                }
            )
        return dictGrofers
if __name__=="__main__":
    userInput = input('Enter The Name of Product >>> ')
    obj = Grofers(userInput)
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(50))
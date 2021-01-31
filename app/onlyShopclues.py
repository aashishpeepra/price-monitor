from bs4 import BeautifulSoup
import requests

def productShopclues(string):
    return "%20".join(string.split())

class Shopclues():
    def __init__(self, product):
        self.__product = product
        self.__request='https://www.shopclues.com/search?q='+productShopclues(product)
        sclRespond = requests.post('https://www.shopclues.com/search?q='+productShopclues(product)).text
        soup = BeautifulSoup(sclRespond, 'lxml')
        self.__soup = soup

    def get_first_price(self):
        # bodyTag = self.__soup.find('html').text
        try:
            strPrice = self.__soup.find('span', class_='p_price').text[3:]
            price = int(''.join(strPrice.split(',')))
            return {"price":price,"website":self.__request,"company":"shopclues"}
        except:
            return []

    def get_first_delivery(self):
        return []

    def get_first_price_and_delivery(self):
        try:
            strPrice = self.__soup.find('span', class_='p_price').text[3:]
            price = int(''.join(strPrice.split(',')))
            delivery = '-'
            return {"price":price,"delivery":delivery,"website":self.__request}
        except:
            return []

    def get_first_n_complete(self, n):
        a = 1
        b = 1
        c = 1
        d = 1
        sclListName = []
        sclListPrice = []
        sclListImage =[]
        sclListURL =[]
        for name in self.__soup.find_all('h2'):
            j = name.text
            sclListName.append(j)
            a += 1
            if a>n:
                break
        for price in self.__soup.find_all('span', class_='p_price'):
            try:
                k = price.text
                am = int(''.join(k[3:].split(',')))
                sclListPrice.append(am)
            except:
                sclListPrice.append('None')
            b += 1
            if b>n:
                break
        for image in self.__soup.find_all('div', class_='img_section'):
            try:
                k = image.img['src']
                sclListImage.append(k)
            except:
                sclListImage.append('None')
            c += 1
            if c>n:
                break
        for URL in self.__soup.find_all('div', class_='col3'):
            try:
                k = URL.a['href']
                sclListURL.append(k)
            except:
                sclListURL.append('None')
            d += 1
            if d>n:
                break
        # print(sclListName)
        # print(sclListPrice)
        # print(sclListImage)
        # print(sclListURL)
        dicti = []
        for m in range(len(sclListName)):
            dicti.append(
                {
                    "name":sclListName[m],
                    "price":sclListPrice[m],
                    "image":sclListImage[m],
                    "url":sclListURL[m]
                }
            )
        return dicti
if __name__=="__main__":
    userInput = input('Enter The Name of Product >>> ')
    obj = Shopclues(userInput)
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(5))
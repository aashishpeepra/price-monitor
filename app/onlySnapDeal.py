from bs4 import BeautifulSoup
import requests

def productSnapdeal(string):
    return "%20".join(string.split())

class Snapdeal():
    def __init__(self, product):
        self.__product = product
        self.__request = 'https://www.snapdeal.com/search?keyword='+productSnapdeal(product)
        snpRespond = requests.post('https://www.snapdeal.com/search?keyword='+productSnapdeal(product)).text
        soup = BeautifulSoup(snpRespond, 'lxml')
        self.__soup = soup

    def get_first_price(self):
        try:
            strPrice = self.__soup.find('span', class_='product-price').text[5:]
            price = int(''.join(strPrice.split(',')))  
            name = self.__soup.find('p', class_='product-title').text.strip()
            return {"price":price,"website":self.__request,"name":name,"company":"snapdeal"}
        except:
            return []

    def get_first_delivery(self):
        return []

    def get_first_price_and_delivery(self):
        try:
            strPrice = self.__soup.find('span', class_='product-price').text[5:]
            price = int(''.join(strPrice.split(',')))
            delivery = '-'
            return {"price":price,"delivery":delivery,"website":self.__request}
        except:
            return []

    def get_first_n_complete(self, n):
        b = 1
        d = 1
        snpListName = []
        snpListPrice = []
        snpListImage =[]
        snpListURL =[]
        title=self.__soup.find_all('p', class_='product-title')
        for i in range(min(n,len(title))):
            snpListName.append(title[i].text)
        for price in self.__soup.find_all('span', class_='product-price'):
            try:
                k = price.text
                am = int(''.join(k[5:].split(',')))
                snpListPrice.append(am)
            except:
                snpListPrice.append('None')
            b += 1
            if b>n:
                break
        images = self.__soup.find_all('img', class_='product-image')
        for i in range(min(n, len(images))):
            try:
                snpListImage.append(images[i]["src"])
            except:
                snpListImage.append(images[i]["data-src"])
        for URL in self.__soup.find_all('div', class_='product-tuple-image'):
            try:
                k = URL.a['href']
                snpListURL.append(k)
            except:
                snpListURL.append('None')
            d += 1
            if d>n:
                break
        dictSnapdeal = []
        for m in range(len(snpListName)):
            dictSnapdeal.append(
                {
                    "name":snpListName[m],
                    "price":snpListPrice[m],
                    "image":snpListImage[m],
                    "url":snpListURL[m]
                }
            )
        return dictSnapdeal
if __name__=="__main__":
    userInput = input('Enter The Name of Product >>> ')
    obj = Snapdeal(userInput)
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(6))
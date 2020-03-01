from bs4 import BeautifulSoup
import requests

def productSnapdeal(string):
    return "%20".join(string.split())

class Snapdeal():
    def __init__(self, product):
        self.__product = product
        self.__request='https://www.snapdeal.com/search?keyword='+productSnapdeal(product)
        snpRespond = requests.post('https://www.snapdeal.com/search?keyword='+productSnapdeal(product)).text
        soup = BeautifulSoup(snpRespond, 'lxml')
        self.__soup = soup

    def get_first_price(self):
        try:
            strPrice = self.__soup.find('span', class_='product-price').text[5:]
            price = int(''.join(strPrice.split(',')))  
            return {"price":price,"website":self.__request}
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
        a = 1
        b = 1
        c = 1
        d = 1
        snpListName = []
        snpListPrice = []
        snpListImage =[]
        snpListURL =[]
        # counter=0
        # for name in self.__soup.find_all('p', class_='product-title'):
        #     counter += 1
        # print(">>>",counter)
        for name in self.__soup.find_all('p', class_='product-title'):
            j = name.text
            snpListName.append(j)
            a += 1
            if a>n:
                break
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
        for image in self.__soup.find_all('img', class_='product-image'):
            try:
                k = image['src']
                snpListImage.append(k)
            except:
                snpListImage.append('None')
            c += 1
            if c>n:
                break
        for URL in self.__soup.find_all('div', class_='product-tuple-image'):
            try:
                k = URL.a['href']
                snpListURL.append(k)
            except:
                snpListURL.append('None')
            d += 1
            if d>n:
                break
        dicti = []
        for m in range(len(snpListName)):
            dicti.append(
                {
                    "name":snpListName[m],
                    "price":snpListPrice[m],
                    "image":snpListImage[m],
                    "url":snpListURL[m]
                }
            )
        return dicti
if __name__=="__main__":
    userInput = input('Enter The Name of Product >>> ')
    obj = Snapdeal(userInput) # Enter Name of Product
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(5))
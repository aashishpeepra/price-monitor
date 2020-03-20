from bs4 import BeautifulSoup
import requests

def productAmazon(string):
     return "=".join(string.split())

class AmazonPantry():
    def __init__(self,product):
        self._product = product
        amzrespond=requests.post("https://www.amazon.in/s?k="+ productAmazon(product)+"&i=pantry").text
        print("https://www.amazon.in/s?k="+ productAmazon(product)+"&i=pantry")
        print(amzrespond)
        soup = BeautifulSoup(amzrespond,'lxml')
        self.__soup=soup
    
    def get_first_price(self):
        try:
            strPrice = self.__soup.find('span', class_='a-price-whole').text[1:]
            price = int(''.join(strPrice.split(',')))  
            return price
        except:
            return []

    def get_first_delivery(self):
        return []

    def get_first_price_and_delivery(self):
        try:
            strPrice = self.__soup.find('span', class_='a-price-whole').text[1:]
            price = int(''.join(strPrice.split(',')))
            delivery = '-'
            return [price,delivery]
        except:
            return []

    def get_first_n_complete(self, n):
        b = 1
        amzListName = []
        amzListPrice = []
        amzListURL =[]
        # title = self.__soup.find_all('a', class_='a-size-base-plus a-color-base a-text-normal')
        # for i in range(min(n,len(title))):
        #     amzListName.append(title[i].text)
        for price in self.__soup.find_all('span', class_='a-price-whole'):
            try:
                k = price.text
                am = int(''.join(k[1:].split(',')))
                amzListPrice.append(am)
            except:
                amzListPrice.append('None')
            b += 1
            if b>n:
                break
        for URL in self.__soup.find_all('a', class_='a-link-normal a-text-normal'):
            try:
                k = URL['href']
                amzListURL.append(str('https://www.amazon.in/')+str(k))
            except:
                amzListURL.append('None')
        dictAmazon = []
        for m in range(len(amzListPrice)):
            dictAmazon.append(
                {
                    #"name":amzListName[m],
                    "price":amzListPrice[m],
                    "url":amzListURL[m]
                }
            )
        return dictAmazon
if __name__=="__main__":
    userInput = input('----Enter The Name of Product---- ')
    obj = AmazonPantry(userInput)
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(50))
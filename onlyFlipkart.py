from bs4 import BeautifulSoup
import requests

def productFlipkart(string):
    return '+'.join(string.split())

class Flipkart():
    def __init__(self, product):
        self.__product = product
        self.__request='https://www.flipkart.com/search?q='+productFlipkart(product)
        flpRespond = requests.post('https://www.flipkart.com/search?q='+productFlipkart(product)).text
        soup = BeautifulSoup(flpRespond, 'lxml')
        self.__soup = soup

    def get_first_price(self):
        try:
            strPrice = self.__soup.find('div', class_='_1vC4OE').text[1:]
            price = int(''.join(strPrice.split(',')))
        except:
            strPrice = self.__soup.find('div', class_='_1vC4OE').text[1:]
            price = int(''.join(strPrice.split(',')))
        name = self.__soup.find('div', class_='_3wU53n')
        if name != None:   # Mobile
            name = name.text
        else:
            name = self.__soup.find('a', class_='_2cLu-l')    # Laptop
            name = name.text
        # print(name)
        return {"price":price,"website":self.__request,"name":name}

    def get_first_delivery(self):
        delivery = '-'
        return delivery

    def get_first_price_and_delivery(self):
        try:
            strPrice = self.__soup.find('div', class_='_1vC4OE').text[1:]
            price = int(''.join(strPrice.split(',')))
        except:
            strPrice = self.__soup.find('div', class_='_1vC4OE').text[1:]
            price = int(''.join(strPrice.split(',')))
        delivery = '-'
        return {"price":price,"delivery":delivery,"website":self.__request}

    def get_first_n_complete(self, n):
        a = 1
        b = 1
        c = 1
        d = 1
        flpListName = []
        flpListPrice = []
        flpListImage =[]
        flpListURL =[]
        for price in self.__soup.find_all('div', class_='_1vC4OE'):
                m = price.text[1:]
                try:
                    price1 = int(''.join(m.split(',')))
                    flpListPrice.append(price1)
                except:
                    flpListPrice.append('None')
                b += 1
                if b>n:
                    break
        for image in self.__soup.find_all('img', class_='_1Nyybr'):
                try:
                    flpListImage.append(str('https:')+str(image['src']))
                except:
                    flpListImage.append('None')
                c += 1
                if c>n:
                    break
        soupName = self.__soup.find_all('div', class_='_3wU53n') # Mobile
        if soupName == []:
            soupName = self.__soup.find_all('a', class_='_2cLu-l')
            for name in soupName:
                k = name.text
                flpListName.append(k)
                a += 1
                if a>n:
                    break
        else:  # Mobile
            for name in soupName:
                p = name.text
                flpListName.append(p)
                a += 1
                if a>n:
                    break
        soupURL = self.__soup.find_all('a', class_='_31qSD5')  #Mobile
        if soupURL == []:
            soupURL = self.__soup.find_all('a', class_='_2cLu-l')
            for URL in soupURL:
                flpListURL.append(str('https://flipkart.com')+str(URL['href']))
                d += 1
                if d>n:
                    break
        else:
            for URL in soupURL:
                flpListURL.append(str('https://flipkart.com')+str(URL['href']))
                d += 1
                if d>n:
                    break
        dictFlipkart = []
        for m in range(len(flpListURL)):
            dictFlipkart.append(
                {
                    "name":flpListName[m],
                    "price":flpListPrice[m],
                    "image":flpListImage[m],
                    "url":flpListURL[m]
                }
            )
        return dictFlipkart
if __name__ == "__main__":
    userInput = input('Enter The Name of The Product >>> ')
    obj = Flipkart(userInput)
    print(obj.get_first_price())
    print(obj.get_first_delivery())
    print(obj.get_first_price_and_delivery())
    print(obj.get_first_n_complete(6))
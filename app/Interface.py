from onlyFlipkart import Flipkart
from onlyShopclues import Shopclues
from onlySnapDeal import Snapdeal
from onlyGrofers import Grofers
from amazonPantry import AmazonPantry
from only2Gud import TwoGud
from onlyPaytm import Paytm
def prices(shopName,item):
    """
    pre: shopName is a valid name form the classes above
    post: returns the price extracted from that website as an integer
    """
    if shopName=="flipkart":
        return Flipkart(item).get_first_price()
    elif shopName=="shopclues":
        return Shopclues(item).get_first_price()
    elif shopName=="snapdeal":
        return Snapdeal(item).get_first_price()
    elif shopName=="grofers":
        return Grofers(item).get_first_price()
    elif shopName=="amazonpantry":
        return AmazonPantry(item).get_first_price()
    elif shopName=="twogud":
        return TwoGud(item).get_first_price()
    elif shopName=="paytm":
        return Paytm(item).get_first_price()
    else:
        return None

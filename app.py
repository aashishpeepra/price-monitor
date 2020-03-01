import flask
import threading
from flask import jsonify as json 
from Interface import prices
import time
from validations import Validate

app=flask.Flask(__name__)
#app.config["DEBUG"]=True
avg=0.0
cnt=0
class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        print("Ran")
        print(self.args)
        self.ref=self.func(*self.args)
    def getRef(self):
        return self.ref
@app.route("/info",methods=["GET"])
def showItems():
    t1=time.time()
    item=flask.request.args.get("item")
    shops=flask.request.args.get("shops")
    obj=Validate(flask.request)
    validationOutcome=obj.validate_prices()
    if validationOutcome=={}:
        shops=shops.split(",")
        threads=[]
        for i in range(len(shops)):
            threads.append(MyThread(prices,(shops[i],item),prices.__name__))
        for i in range(len(shops)):
            threads[i].start()
        data=[]
        for i in range(len(shops)):
            threads[i].join()
            data.append(threads[i].getRef())
        data.append({"time":time.time()-t1})
        return json(data)
    else:
        return json(validationOutcome)
    return "<h1>Price of {} on <br/> Shopclues : {} <br/> SnapDeal : {} <br/> Flipkart : {} <br/> Time : {} </h1>".format(item,shopObj.get_first_price(),snapObj.get_first_price(),flipObj.get_first_price(),time.time()-t1)
@app.route("/",methods=["GET"])
def home():
    return json({"header":"HomePage","author":"Ironprogrammers","content":"Read Documentation for usage"})
@app.route("/price",methods=["GET"])
def route_to_price():
    t1=time.time()
    obj=Validate(flask.request)
    validationResult=obj.validate_single_price()
    if not validationResult :
        item=flask.request.args.get("item")
        shopName=flask.request.args.get("shop")
        value=prices(shopName,item)
        if type(value)==type({}) and len(list(value.keys()))==3 and value!=None:
            global avg
            global cnt
            avg+=time.time()-t1
            cnt+=1
            return json({"website":shopName,"data":{"price":value["price"],"url":value["website"]},"time":time.time()-t1})
        else:
            return json({"error":{"title":"Item not found","type":"input error"}})
    else:
        return json(validationResult)

if __name__=="__main__":
    app.run()   
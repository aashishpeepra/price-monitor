import flask
from onlyShopclues import Shopclues
from onlySnapDeal import Snapdeal
app=flask.Flask(__name__)
app.config["DEBUG"]=True

@app.route("/info",methods=["GET"])
def showItems():
    item=flask.request.args.get("item")
    method=flask.request.args.get("method")
    print(item)
    item=item[:item.index("?")]
    shopObj=Shopclues(item)
    print(shopObj.get_first_price())
    snapObj=Snapdeal(item)
    print(snapObj.get_first_price())
    return "<h1>Price of {} on <br/> Shopclues : {} <br/> SnapDeal : {} </h1>".format(item,shopObj.get_first_price(),snapObj.get_first_price())
@app.route("/",methods=["GET"])
def home():
    return "<h1>Flask</h1>"
app.run()
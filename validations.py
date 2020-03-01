"""
This File contains all the code for the validation of the requests that will be done to the API
"""
import urllib.parse as URL
class Validate():
    def __init__(self,query):
        self._query=query
        self._error={}
        self._price_params=["item","shop","category"]
        self._shops=["flipkart","amazon","shopclues","snapdeal","grofers","paytm","twogud"]
    def validate_url(self):
        decodes=""
        updatedQuery=str(self._query)[str(self._query).index("\'"):str(self._query).rindex("\'")]
        try:
            decodes=URL.parse_qs(updatedQuery)
        except:
            try:
                decodes=URL.parse_qs(updatedQuery)
            except:
                self._error.update({"error":{"title":"Received request isn't encoded correctly","type":"url"}})
        return self._error
    def validate_shop(self,shop):
        return any([each==shop for each in self._shops])
    def validate_params(self,param):
        return all([self._query.args.get(name) for name in param])
    def validate_single_price(self):
        try:
            self.validate_url()
            if self.validate_params(self._price_params[:-1]) and not self.validate_url():
                data=[self._query.args.get(name) for name in self._price_params]
                if (type(data[0])==type("") and len(data[0])>0) and (type(data[1])==type("") and len(data[1])>0):
                    if not (len(data[1])<15 and self.validate_shop(data[1])):
                        self._error={"error":{"title":"Received shop paramater doesn't exist","type":"param","expected":"Valid Shop Name"}}
                else:
                    self._error={"error":{"title":"item and shop parameters can't be empty","type":"param","expected":self._price_params}}
            else:
                self._error={"error":{"title":"Insufficient Params Passed","type":"param","expected":self._price_params}}
        except:
            self._error={"error":{"title":"Some Error Occured","type":"unknown"}}
        return self._error
    def validate_prices(self):
        item=self._query.args.get("item")
        shops=self._query.args.get("shops")
        if item==None or shops==None or item=="" or shops=="":
            self._error={"error":{"title":"Item or Shop can't be empty"}}
            return self._error
        if "," not in shops and self.validate_shop(shops):
            return {}
        elif "," in shops and shops[0]!="," and len(shops.split(","))!=0:
            shops=shops.split(",")
            correct=False
            for each in shops:
                correct=self.validate_shop(each)
            if correct:                    
                return {}
            else:
                return {"error":{"title":"Passed shop name didn't matched","expected":"Pass valid shop names"}}
        else:
            return {"error":{"title":"Take care of the commas","expected":"Expected a valid shop name or names comma seperated"}}

            
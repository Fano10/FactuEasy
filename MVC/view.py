from flask import make_response, jsonify
from MVC.model import Bill, Product

class ViewAllBill(object):
    
    def __init__ (self,allBill):
        self.allBill = allBill

    def response(self):
        dictArray = []
        for bill in self.allBill:
            dictBill = {"id":bill.id,"name":bill.name,"date":bill.date,"total":bill.total}
            dictArray.append(dictBill)
        data = {"products":dictArray}
        #Creer un objet de reponse avec JSON, code de statut et en-tetes
        response = make_response(jsonify(data))
        response.status_code = 200 
        response.headers['Content-Type'] ='application/json'
        return response
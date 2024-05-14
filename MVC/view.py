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
        data = {"bills":dictArray}
        #Creer un objet de reponse avec JSON, code de statut et en-tetes
        response = make_response(jsonify(data))
        response.status_code = 200 
        response.headers['Content-Type'] ='application/json'
        return response

class ViewProducts(object):

    def __init__(self,products):
        self.products = products

    def response(self):
        dictArray = []
        for product in self.products:
            dictProduct = {"id":product.id,"idBill":product.idBill,"name":product.name,"price":product.price}
            dictArray.append(dictProduct)
        data = {"products": dictArray}
        #Creer un objet de reponse avec JSON, code de statut et en-tetes
        response = make_response(jsonify(data))
        response.status_code = 200 
        response.headers['Content-Type'] ='application/json'
        return response
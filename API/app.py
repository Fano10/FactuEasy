from flask import Flask
from flask_cors import CORS
from MVC.model import *
from MVC.service import *
from MVC.view import ViewAllBill,ViewProducts

app = Flask(__name__)
CORS(app) #Activer CORS pour toutes les routes
init_app(app)


@app.route('/')
def index():
    return "Welcome to FactuEasy"

@app.route('/allBill')
def getBill():
    bills = Bill.select()
    response = ViewAllBill(bills)
    return response.response()

@app.route('/billProducts/<int:bill_id>')
def getProductsByBill(bill_id):
    products = ServiceGetProductByBill(bill_id)
    response = ViewProducts(products.execute())
    return response.response()


if __name__ =='__main__':
    app.run(debug =True)

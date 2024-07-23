from flask import Flask, request ,jsonify
from flask_cors import CORS
from MVC.model import *
from MVC.service import *
from MVC.view import all_response

app = Flask(__name__)
CORS(app, supports_credentials=True) #Activer CORS pour toutes les routes
init_app(app)

g_userCookie = {} # paire cle valeur de cookie et d'id user

@app.route('/')
def index():
    idUser = get_cookie(request,g_userCookie) # recuperer l'utilisateur
    if idUser == -1 : # si l'utilisateur n'existe pas
        data = {
            "success":False
        }
        return all_response(data,401,'')
    return all_response({"success":True},200,'')

@app.route('/login', methods = ['POST'])
def login():
    try:
        data = request.json # récupère le fichier json de la requete
        response = authentification(data,g_userCookie)
        return all_response(response['data'],response['code'],response['cookie'])
    except:
        return all_response({"success":False},401,"")

@app.route('/allBill')
def getBill():
    idUser = get_cookie(request,g_userCookie) # recuperer l'utilisateur
    if idUser == -1 : # si l'utilisateur n'existe pas
        data = {
            "success":False
        }
        return all_response(data,401,'')

    response = all_bill(idUser)
    return all_response(response,200,g_userCookie[idUser])

@app.route('/billProducts/<int:bill_id>')
def getProductsByBill(bill_id):
    idUser = get_cookie(request,g_userCookie) # recuperer l'utilisateur
    if idUser == -1 : # si l'utilisateur n'existe pas
        data = {
            "success":False
        }
        return all_response(data,401,'')
    products = get_product_by_bill(bill_id)
    response = all_products_dict(products)
    return all_response(response,200,g_userCookie[idUser])

@app.route('/products')
def getProducts():
    idUser = get_cookie(request,g_userCookie) # recuperer l'utilisateur
    if idUser == -1 : # si l'utilisateur n'existe pas
        data = {
            "success":False
        }
        return all_response(data,401,'')
    products = Product.select().where(Product.idUser == idUser)
    response = all_products_dict(products)
    return all_response(response,200,g_userCookie[idUser])

@app.route('/addBill' , methods = ['POST'])
def addBill():
    idUser = get_cookie(request,g_userCookie) # recuperer l'utilisateur
    if idUser == -1 : # si l'utilisateur n'existe pas
        data = {
            "success":False
        }
        return all_response(data,401,'')
    try:
        data = request.get_json()
        insert_bill(data,idUser)
        return all_response({"success":True},200,g_userCookie[idUser])
    except:
        return all_response({"success":False},422,"")
    
if __name__ =='__main__':
    app.run(debug =True,host='0.0.0.0', port=5000)

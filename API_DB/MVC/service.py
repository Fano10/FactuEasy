from MVC.model import Bill,Product,Users
import json
import hashlib
import secrets
from datetime import datetime

def get_product_by_bill(idBill):
    """
    Récupère les produits ou achats avec le id du facture

    Paramètre:
        idBill(int) : id du facture
    
    Retour:
        products(Peewee ModelSelect) : requete construite mais non executé. Il suffit d'itérer dessus pour exectuer la requete et récuperer les instances des produits
    """
    products = Product.select().where(Product.idBill == idBill) #select plusieurs resultat tandis que get un seul resultat

    return products


def all_products_dict(products):
    """
    Transforme des instances de produits en dictionnaire

    Paramètres:
        products(Peewee ModelSelect): requete à executer et à itérer

    Retour:
        data(array of dict): avec les clés : id, idBill, name, description et price 
    """
    dictArray = []
    for product in products:
        dictProduct = {"id":product.id,"idBill":product.idBill,"name":product.name,"description":product.description,"price":product.price}
        dictArray.append(dictProduct)
    data = {"products": dictArray}
    return data


def getJson(): # simule le fait que l'API qui contient l'IA a envoyer son retour
    product = ["viande","legume"]
    prix = ["15","12"]
    data = {"products":product , "prices":prix}
    data = {"resultat":data}
    return data

def authentification(data, userCookie):
    """
    Vérifie l'information envoyé par l'utilisateur par celle qui sont dans la base de donnée

    paramètres:
        data(dictionnaire): avec les clés username et password
        userCookie(dictionnaire): avec le clé idUser

    retour:
        dictionnaire : avec les clés: data, code et cookie

    """
    userName = data['username']
    password = data['password'].encode('UTF-8')
    #Creer l'objet de hachage
    hashObject = hashlib.sha256()
    #Mettre a jour l'objet avec les donnees
    hashObject.update(password)
    #Obtenir le hachage sous forme hexadecimale
    hashHex = hashObject.hexdigest()

    try:
        user = Users.get(Users.username == userName)
        if user.password == hashHex:
            #Generation d'une valeur aleatoire de cookie
            randomValue = secrets.token_urlsafe(16)
            #ajout du cookie dans le dictionnaire de userCookie
            userCookie[user.id] = randomValue
            return {"data":{"success":True},"code":200,"cookie":randomValue}
        else:
            return {"data":{"success":False},"code":401,"cookie":""}
    except:
        return {"data":{"success":False},"code":401,"cookie":""}
    
def get_cookie(request, userCookie):
    """
    Chercher l'id de l'utilsateur qui correspond au cookie dans la requete

    Paramètre:
        request(object) : la requete de l'utilisateur
        userCookie(dict) : contient la relation idUser-Cookie

    Retour:
        idUser(int): retourne l'id si le cookie correspond sinon retourne -1

    """
    
    idUser = -1
    try:
        cookie = request.cookies.get('userCookie')
        for key,value in userCookie.items():
            if cookie == value:
                idUser = key
        return idUser
    except:
        return idUser

def insert_bill(data, idUser):
    """
    Insérer une nouvelle facture avec ces produits dans la base de données

    Paramètres:
        data(dict): avec les clés articles et prix
        idUser(int) : id de l'utilisateur
    
    Retour:
        null : ne retourne rien
    """
    #Inserer une nouvelle facture
    articles = data['articles']
    prix = data ['prix']
    taille = len(articles) # nombres d'articles
    total = 0.0
    #Création et insértion de la nouvelle facture
    for i in range(taille):
        total += float(prix[i])
    newBill = Bill.create(
        name = 'Maxi',
        idUser = idUser,
        date = datetime.today().strftime('%Y-%m-%d'),
        total = total
    )
    #Insértion des produits
    for i in range (taille):
        Product.create(
            name = articles[i],
            description = '',
            idBill = newBill.id,
            idUser = idUser,
            price = prix[i]
    )

def all_bill(idUser):
    """
    Recuperer toutes les factures d'un utilisateur 

    Paramètres:
        idUser(int) : id de l'utilisateur 

    Retour:
        data(dict) : avec les clés: id, name, date et total
    """

    bills = Bill.select().where(Bill.idUser == idUser)
    dictArray = []
    for bill in bills:
            dictBill = {"id":bill.id,"name":bill.name,"date":bill.date,"total":bill.total}
            dictArray.append(dictBill)
    data = {"bills":dictArray}
    return data


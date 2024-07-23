from flask import Flask, render_template,request,make_response,jsonify,Response
from urllib.request import urlopen,Request
import urllib.request
import json
import requests
import os
from MVC import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True) #Active CORS avec support pour les credentials
URL_API_DB = os.environ.get('URL_API_DB')
URL_API_IA = os.environ.get('URL_API_IA')

def proxy(url, request):
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_data() if request.method in ['POST', 'PUT', 'PATCH'] else None
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        params=request.args,
        data=data,
        cookies=request.cookies
    )
    flask_response = Response(response.content, status=response.status_code)
    for key, value in response.headers.items():
        flask_response.headers[key] = value

    return flask_response  

@app.route('/')
def index():
    try:    
        cookie = request.cookies.get('userCookie')
        cookie_key_value = 'userCookie=' + cookie
        url = URL_API_DB
        headers = {'Cookie': cookie_key_value}
        req = urllib.request.Request(url, headers= headers)
        response = urlopen(req)
        return render_template('index.html')
    except:
        return render_template('login.html')
    

@app.route('/allBills')
def getAllBills():
    return render_template('allBills.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/item/<int:item_id>')
def getItemById(item_id):
    try:
        cookie = request.cookies.get('userCookie')
        cookie_key_value = 'userCookie=' + cookie
        url = URL_API_DB+'/billProducts/' + str(item_id)
        headers = {'Cookie': cookie_key_value}
        req = urllib.request.Request(url, headers= headers)
    
        response = urlopen(req)
        headers = response.headers
        jsonData = response.read()
        assert headers["Content-Type"] == 'application/json' #vérifier qu'on a bien obtenu un JSON
        dictData = json.loads(jsonData)
        data = dictData["products"]
        return render_template('item.html',data = data)
    except:
        response = make_response(jsonify({"success":False}))
        response.status_code = 500
        response.headers['Content-Type'] ='application/json'
        return response
    
@app.route('/allItem')
def getItem():
    cookie = request.cookies.get('userCookie')
    cookie_key_value = 'userCookie=' + cookie
    url = URL_API_DB+'/products'
    headers = {'Cookie': cookie_key_value}
    req = urllib.request.Request(url, headers= headers)
    try:
        response = urlopen(req)
        headers = response.headers
        jsonData = response.read()
        assert headers["Content-Type"] == 'application/json' #vérifier qu'on a bien obtenu un JSON
        dictData = json.loads(jsonData)
        data = dictData["products"]
        return render_template('item.html',data = data)
    except:
        response = make_response(jsonify({"success":False}))
        response.status_code = 500
        response.headers['Content-Type'] ='application/json'
        return response


@app.route('/upload', methods = ['POST'])
def uplodImg():
    url = URL_API_IA
    return proxy(url, request)

@app.route('/authentification', methods = ['POST'])
def authentification():
    url = URL_API_DB+'/login'
    return proxy(url, request)

@app.route('/apiAddBills', methods = ['POST'])
def apiAddBills():
    url = URL_API_DB+'/addBill'
    return proxy(url, request)


@app.route('/apiAllBills')
def apiAllBills():
    cookie = request.cookies.get('userCookie')
    cookie_key_value = 'userCookie=' + cookie
    url = URL_API_DB+'/allBill'
    headers = {'Cookie': cookie_key_value}
    req = urllib.request.Request(url, headers= headers)
    try:
        response = urlopen(req)
        return response
    except:
        response = make_response(jsonify({"success":False}))
        response.status_code = 401
        response.headers['Content-Type'] ='application/json'
        return response

if __name__ =='__main__':
    app.run(debug =True,host='0.0.0.0', port=8080)
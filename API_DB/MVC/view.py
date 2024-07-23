from flask import make_response, jsonify
from MVC.model import Bill, Product

def all_response(data, code, cookie):
    response = make_response(jsonify(data))
    response.status_code = code
    response.headers['Content-Type'] ='application/json'
    response.set_cookie('userCookie',cookie, httponly=True)
    return response
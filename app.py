from flask import Flask
from MVC.model import *

app = Flask(__name__)
init_app(app)

@app.route('/')
def index():
    return "Welcome to FactuEasy"


if __name__ =='__main__':
    app.run(debug =True)

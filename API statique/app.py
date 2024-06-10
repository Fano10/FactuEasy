from flask import Flask, render_template
from MVC import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('allBills.html')
    #return "Hello world"

if __name__ =='__main__':
    app.run(debug =True, port=8080)
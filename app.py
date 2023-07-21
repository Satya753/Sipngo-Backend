import os
from flask import Flask , render_template , request , url_for , redirect
import mysql.connector
import sys
from flask_cors import CORS
sys.path.append('models/')
from Category import Category
from Models import Model

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME")
)


models = Model(db)


@app.route("/home")
def fetchCategories():
    d = models.getCategories()
    item = []
    for data in d:
        item.append(data.getName())
        print(data.getName())

    return item




if __name__=="__main__":
    app.run()







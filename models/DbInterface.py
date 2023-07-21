import os
from flask import Flask , render_template , request , url_for , redirect

import mysql.connector


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'loca34lhost'
app.config['MYSQL_USER'] = 'root23423'
app.config['MYSQL_PASSWORD'] = 'Hell234234234oworld@123'
app.config['MYSQL_DB'] = 'sipngo'


db = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME")
)




def getCategories():
    cursor = db.cursor()
    cursor.execute(''' SELECT * from category ''')
    data = cursor.fetchall()
    cursor.close()

    return data


print(getCategories())


import os
from flask import Flask ,  render_template , request ,jsonify, url_for , redirect
import mysql.connector
import sys
from flask_cors import CORS
sys.path.append('models/')
sys.path.append('Utils/')
from Category import Category
from Models import Model
from ImageProcessing import ByteImage 
from dotenv import load_dotenv
from mysql.connector import pooling
load_dotenv()

app = Flask(__name__)
CORS(app)


connection_pool = pooling.MySQLConnectionPool(host = os.environ["DB_HOST"],
        user = os.environ["DB_USER"],
        password = os.environ["DB_PASSWORD"],
        database = os.environ["DB_NAME"],
        pool_name = "my_sql_pool",
        pool_size = 5,
        pool_reset_session = True
        )


#db = MySQLPool(app)




def getNewConnection(db):
    conn = db.get_connection()
    return conn 

@app.route("/home")
def fetchCategories():
    conn = getNewConnection(connection_pool)
    models = Model(conn)
    d = models.getCategories()
    item = []
    for data in d:
        if data.image==None:
            data.image = 'static/items/download.jpeg'
        byteimg = ByteImage(data.image)
        item.append([data.getName() , data.getId() , byteimg.getBase64()])
    conn.close()

    print(item)

    return item

@app.route("/home/category" , methods = ['GET'])
def fetchItems():
    conn = getNewConnection(connection_pool)
    models = Model(conn)
    category_id = request.args.get('id')
    items = models.getItems(category_id)
    res = []

    for item in items:
        byteimg = ByteImage(item.image_path)
        res.append([item.price , item.name ,byteimg.getBase64() , item.id])

    conn.close()

    return res


@app.route("/home/add_order" , methods = ['POST'])
def addOrder():
    conn = getNewConnection(connection_pool)
    data = request.json
    # Insert data into table 
    print(data)
    status = models.addOrder(data)

    response  = {
            'message':'Order placed successfully , Track with below order id',
            'order_id':'1XE3'
        }
    conn.close()
    return jsonify(response , 200)




if __name__=="__main__":
    app.run(host='0.0.0.0' , port=5000)







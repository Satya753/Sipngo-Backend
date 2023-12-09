import os
import json
from flask import Flask ,  render_template , request ,jsonify, url_for , redirect
import mysql.connector
import sys
from flask_cors import CORS
sys.path.append('service/')
sys.path.append('models/')
from AuthModel import UserAuth
from PhonePe import PhonePe
sys.path.append('Utils/')
from Category import Category
from Models import Model
from ImageProcessing import ByteImage 
from dotenv import load_dotenv
from mysql.connector import pooling
import logging
load_dotenv()
#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
CORS(app)


connection_pool = pooling.MySQLConnectionPool(host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        pool_name = "my_sql_pool",
        pool_size = 5,
        pool_reset_session = True
        )

app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASS'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_NAME") 
app.config['MYSQL_POOL_NAME'] = 'mysql_pool'
app.config['MYSQL_POOL_SIZE'] =32 
app.config['MYSQL_AUTOCOMMIT'] = True

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
        # Change
        item.append({'name':data.getName() , 'id':data.getId() , 'img':byteimg.getBase64()})
    conn.close()

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
        res.append({'price':item.price , 'name':item.name , 'img':byteimg.getBase64() , 'id':item.id})
        #res.append([item.price , item.name ,byteimg.getBase64() , item.id])

    conn.close()

    return res


@app.route("/home/add_order" , methods = ['POST'])
def addOrder():
    conn = getNewConnection(connection_pool)
    data = request.json
    models = Model(conn)
    # Insert data into table 
    print(data)
    order_id = models.addOrder(data)
    print(order_id)

    response  = {
            'message':'Order placed successfully , Track with below order id',
            'order_id':order_id
        }
    conn.close()
    return jsonify(response , 200)


@app.route("/home/signUp" , methods = ['POST'])
def addNewUser():
    conn = getNewConnection(connection_pool)
    data = request.json
    userauth = UserAuth(conn)
    status = userauth.insertNewUser(data)
    response = {
            'message' : 'User  added succesfull'
            }
    conn.close()

    return jsonify(response , 200)


@app.route("/home/subscription" , methods = ['GET'])
def getSubscriptionDetails():
    conn = getNewConnection(connection_pool)
    models = Model(conn)
    user_id = request.args.get('user_id') 
    sub_details = models.getSubscriptionPerUser(user_id)
    #order_details = models.getSubscriptionOrderDetail(user_id)
    conn.close()

    return sub_details

@app.route("/home/userLocation" , methods = ['POST'])
def userLocation():
    conn  = getNewConnection(connection_pool)
    models = Model(conn)
    status = models.addUserLocation(request.json)

    return status

@app.route("/home/payment" , methods= ['POST'])
def paymentTransaction():
    transactionDetail = request.json
    phonepe= PhonePe()
    response = phonepe.payRequest(request.json)
    if response['success']==True:
        conn = getNewConnection(connection_pool)
        models = Model(conn)
        data = {'user_id':request.json["user_id"] , 'id':response['data']['merchantTransactionId']}
        models.initiateTransaction(data)
        return response
    else:
        return response


if __name__=="__main__":
    app.run(host='0.0.0.0' , port=5000)







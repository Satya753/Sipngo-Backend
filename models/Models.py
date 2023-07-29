import os
from flask import Flask , render_template , request , url_for , redirect
import mysql.connector
import sys
sys.path.append('models/')
sys.path.append('../Utils/')
from Category import Category
from Item import Item
import time
from GenerateOrderId import GenerateOrderId

class Model:
    def __init__(self , db):
        self.db = db

    def getCategories(self):
        cursor = self.db.cursor()
        cursor.execute(''' SELECT * from category ''')
        rows = cursor.fetchall()

        category = []

        for row in rows:
            item = Category(row[0] , row[1] , row[2])
            print(item)
            category.append(item)


        return category 


    def getItems(self , category_id):
        cursor = self.db.cursor()
        cursor.execute(""" SELECT name , price , image_path ,  active , id from item where item.category=%s"""%(category_id))
        rows = cursor.fetchall()

        items = []

        for row in rows:
            item = Item(row[0] , row[1] , row[2] , row[3] , row[4])
            items.append(item)

        return items

    def addOrder(self , order_details):
        cursor = self.db.cursor()
        user_id = order_details["user_id"]
        items = order_details["orders"]
        slot = order_details["slot"]
        days = order_details["days"]

        current_timestamp = int(time.time())
        genOrder = GenerateOrderId(user_id ,str(current_timestamp)) 
        order_id = genOrder.getOrderId()

        query = 'INSERT INTO order_detail (order_id, user_id , item_id ,cnt , amount , slot , days) VALUES (%s , %s ,%s , %s , %s , %s , %s)'

        for (id , cnt , amount) in items:
            values = (order_id , user_id , id , cnt , amount , slot , days)
            cursor.execute(query , values)
            self.db.commit()
            print(id , amount)
        print(order_id)





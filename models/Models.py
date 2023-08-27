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
from datetime import datetime

class Model:
    def __init__(self , db):
        self.db = db

    def getCategories(self):
        cursor = self.db.cursor()
        cursor.execute(''' SELECT * from category ''')
        rows = cursor.fetchall()

        category = []
        for row in rows:
            item = Category(row[0] , row[1] , row[2] , row[3])
            category.append(item)


        return category 

    def getSubscriptionPerUser(self , user_id):
        cursor = self.db.cursor()
        print(user_id)
        cursor.execute("""select * from subscription_tracker as s , day_tracker as d where s.sub_id = d.sub_id and d.user_id = '%s'"""%(user_id))
        dayrows = cursor.fetchall()

        return dayrows


    def getSubscriptionOrderDetail(self , user_id):
        cursor = self.db.cursor()
        cursor.execute("""select * from subscription_tracker as s , order_detail as d where s.sub_id= d.sub_id and d.user_id = '%s'"""%(user_id))

        orderrows = cursor.fetchall()
        
        return orderrows

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
        days = len(order_details["days"])

        current_timestamp = int(time.time())
        genOrder = GenerateOrderId(user_id ,str(current_timestamp)) 
        order_id = genOrder.getOrderId()

        query = 'INSERT INTO order_detail (sub_id, user_id , item_id ,cnt , amount , slot , days) VALUES (%s , %s ,%s , %s , %s , %s , %s)'

        for (id , cnt , amount) in items:
            values = (order_id , user_id , id , cnt , amount , slot , days)
            cursor.execute(query , values)
            self.db.commit()
            print(id , amount)


        # Insert subscription details to table so to display it to the user

        subscription_query = 'INSERT INTO subscription_tracker (user_id , sub_id , rem_days , order_placed , total_amount , status) VALUES (%s, %s, %s, %s , %s , %s)'

        sub_values = (user_id , order_id , days , datetime.now() , order_details["total_amount"], "Not Approved")
        cursor.execute(subscription_query , sub_values)
        self.db.commit()


        # Start inserting days for every user to keep track of each and every day

        day_query = 'INSERT INTO day_tracker (location , sub_id , user_id , STATUS , order_date ) VALUES (%s , %s , %s , %s , %s)'

        for day in order_details["days"]:
            location = "Delhi"
#            date_string = day.replace('(India Standard Time)', '').rstrip()
#            date = datetime.strptime(date_string, '%a %b %d %Y %H:%M:%S %Z%z').strftime("%Y-%m-%d %H:%M:%S")
            values = (location, order_id , user_id ,"Not-Delivered" ,day) 
            print(values)
            cursor.execute(day_query , values)
            self.db.commit()
            print(values)
        print(order_id)





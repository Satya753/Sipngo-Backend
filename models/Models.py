import os
from flask import Flask , render_template , request , url_for , redirect
import mysql.connector
import sys
import datetime
sys.path.append('models/')
sys.path.append('../Utils/')
from Category import Category
from Item import Item
import time
from GenerateOrderId import GenerateOrderId
from datetime import datetime
import json

class Model:
    def __init__(self , db):
        self.db = db

    def getCategories(self):

        try:
            cursor = self.db.cursor()
            cursor.execute(''' SELECT * from category ''')
            rows = cursor.fetchall()

            category = []
            for row in rows:
                item = Category(row[0] , row[1] , row[2] , row[3])
                category.append(item)
        except Exception as e:
            return e

        return category 
    
    def getDaysPerUser(self , sub_id , user_id):
        try:
            values = (sub_id , user_id)
            daysQuery = """ select * from day_tracker as d where d.sub_id=%s and d.user_id=%s"""
            cursor = self.db.cursor()
            cursor.execute(daysQuery , values)
            days = cursor.fetchall()
            daysDict = []
            for day in days:
                daysDict.append({"sub_id":day[1] , "order_date":day[3] , "status":day[4]})
        except Exception as e:
            return e
        return daysDict

    def getSubscriptionPerUser(self , user_id):
        try:
            cursor = self.db.cursor()
            print(user_id)
            subIdQuery = """select s.sub_id from subscription_tracker as s where s.status = %s and s.user_id=%s"""
            values  = ("Not Approved" , user_id)
            cursor.execute(subIdQuery , values)
            sub_id = cursor.fetchall()
            print(sub_id[0][0])
            values = (sub_id[0][0] , user_id)
        except Exception as e:
            return e

        #print(dayrows)
        return self.getDaysPerUser(sub_id[0][0] , user_id)

    def getSubscriptionOrderDetail(self , user_id):

        try:
            cursor = self.db.cursor()
            cursor.execute("""select * from subscription_tracker as s , order_detail as d where s.sub_id= d.sub_id and d.user_id = '%s'"""%(user_id))

            rows = cursor.fetchall()
            print(rows)
            subscriptions  = []
            for row in rows:
                subscription = {"rem_days":row[2] , "status":row[3] , "order_placed":row[4] , "status":row[5]}
                subscriptions.append({row[1]:subscription})
        except Exception as e:
            return e
        return subscriptions


        

    def getItems(self , category_id):
        try:
            cursor = self.db.cursor()
            cursor.execute(""" SELECT name , price , image_path ,  active , id from item where item.category=%s"""%(category_id))
            rows = cursor.fetchall()

            items = []

            for row in rows:
                item = Item(row[0] , row[1] , row[2] , row[3] , row[4])
                items.append(item)
        except Exception as e:
            return e
        return items
    def addUserLocation(self , user_location):

        try:
            cursor = self.db.cursor()
            values = (json.dumps(user_location['coords']) , user_location['user_id'])

            query = """UPDATE user_details SET user_location=%s WHERE user_id=%s"""
            print(values)

            cursor.execute(query , values)
            self.db.commit()
        except Exception as e:
            return e
        return "Update successfully"

    def addOrder(self , order_details):

        try:
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
        except Exception as e:
            return e


        # Insert subscription details to table so to display it to the user

        subscription_query = 'INSERT INTO subscription_tracker (user_id , sub_id , rem_days , order_placed , total_amount , status) VALUES (%s, %s, %s, %s , %s , %s)'

        sub_values = (user_id , order_id , days , datetime.now() , order_details["total_amount"], "Not Approved")
        try:
            cursor.execute(subscription_query , sub_values)
            self.db.commit()
        except Exception as e:
            return e


        # Start inserting days for every user to keep track of each and every day

        try:
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
        except Exception as e:
            return e
        print(order_id)
        return order_id
    def initiateTransaction(self , transactionDetail):
        query = 'INSERT INTO UPI_TRANSACTIONS (transactionId , user_id , date_of_transaction , STATUS) VALUES (%s , %s , %s , %s)'
        values = (transactionDetail['id'] , transactionDetail['user_id'] , datetime.now() , 'INITIATED')
        try:
            cursor = self.db.cursor()
            cursor.execute(query , values)
            self.db.commit()
        except Exception as e:
            return e
    def updateTransactionStatus(self , transactionId , status):
        query = """UPDATE UPI_TRANSACTIONS  SET STATUS=%s WHERE transactionId=%s"""
        values  = (status , transactionId)
        print(values)
        try:
            cursor = self.db.cursor()
            rowcount = cursor.execute(query , values)
            print(rowcount)
            self.db.commit()
        except Exception as e:
            print(e)
            return e



#UPDATE UPI_TRANSACTIONS  SET STATUS='99726f32cc5547468ec9391d82a819fb' WHERE transactionId='ERROR';


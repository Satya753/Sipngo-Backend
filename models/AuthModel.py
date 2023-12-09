import os
from flask import Flask 
import mysql.connector

import time
import sys


class UserAuth:

    def __init__(self ,db):
        self.db = db


    def insertNewUser(self , userInfo):
        cursor = self.db.cursor()
        query = 'INSERT INTO user_details (user_id , user_name , user_email , user_location , phone_no) VALUES (%s  , %s , %s , %s , %s)'

        values = (userInfo['user_id'] , userInfo['user_name'] , userInfo['user_email'] , userInfo['user_location'] , userInfo['phone_no'])


        try:
            cursor.execute(query , values)
            self.db.commit()
        except mysql.connector.Error as err:
            print(err)


    def getAllUsers(self):

        cursor = self.db.cursor()

        query = 'SELECT * FROM user_details'

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            print(err)


        return []









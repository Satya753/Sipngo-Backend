import os
from flask import Flask , render_template , request , url_for , redirect
import mysql.connector
import sys
sys.path.append('models/')
from Category import Category


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





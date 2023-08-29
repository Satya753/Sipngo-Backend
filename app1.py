import datetime
from flask import Flask, request, jsonify, g
from datetime import datetime, timedelta
import mysql.connector
from PIL import Image
from werkzeug.utils import secure_filename
import os
import logging
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('new_page.html')

@app.route('/shop')
def store():
    return app.send_static_file('rob.html')

# MySQL configurations

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sipngo'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'sipngo'

# Function to create a MySQL connection
# def db:
#     if 'db' not in g:
#         g.db = mysql.connector.connect(
#             host=app.config['MYSQL_HOST'],
#             user=app.config['MYSQL_USER'],
#             password=app.config['MYSQL_PASSWORD'],
#             database=app.config['MYSQL_DB']
#         )
#     return g.db

# Function to close the MySQL connection
# @app.teardown_appcontext
# def close_db(error):
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()

db = mysql.connector.connect(
  host="localhost",
  user="sipngo",
  password="Password",
  database="sipngo"
)

connection_pool = pooling.MySQLConnectionPool(host="localhost",
  user="sipngo",
  password="Helloworld@123",
  database="sipngo",
  pool_name = 'my_sql_pool',
  pool_size=5,
  pool_reset_session = True
)

# mysql = MySQL(app)

@app.route('/save_data', methods=['POST'])
def save_data():
    # return app.send_static_file('rob.html')
    username = request.form['username']
    password = request.form['password']

    # Save data to MySQL user table
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
    # mysql.connection.commit()
    # cur.close()

    return 'Data saved successfully!'


#################################################
######################STORE API##################
# Route for fetching category details with items
@app.route('/api/categories', methods=['GET'])
def get_categories_with_items():
    try:
        cursor = db.cursor()

        query = '''
        SELECT c.id, c.name, i.id, i.name, i.price, i.image_path
        FROM category c
        LEFT JOIN item i ON c.id = i.category AND i.active = 1
        WHERE c.active = 1
        '''
        cursor.execute(query)

        categories = {}
        for row in cursor.fetchall():
            category_id = row[0]
            category_name = row[1]

            if category_id not in categories:
                categories[category_id] = {
                    'id': category_id,
                    'name': category_name,
                    'items': []
                }

            if row[2] is not None:  # Check if the item is not None (i.e., there is a matching item)
                item = {
                    'id': row[2],
                    'name': row[3],
                    'price': row[4],
                    'image_path': row[5],
                }

                categories[category_id]['items'].append(item)

        cursor.close()

        response = list(categories.values())

        return jsonify(response)
    except Exception as e:
        return str(e), 500


@app.route('/checkout', methods=['POST'])
def checkout():
  # Get the item IDs from the request data
  item_ids = request.json

  # Create a cursor to interact with the database
  cursor = db.cursor()

  try:
    # Insert a new order into the orders table
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO `order` (order_time) VALUES (%s)", (timestamp,))
    order_id = cursor.lastrowid

    # Insert the order items into the order_items table
    for item_id in item_ids:
      cursor.execute("INSERT INTO order_item (order_id, item_id) VALUES (%s, %s)", (order_id, item_id))

    # Commit the changes to the database
    db.commit()

    return jsonify({'message': 'Checkout successful'})

  except Exception as e:
    # Rollback the transaction in case of any error
    db.rollback()
    return jsonify({'error': str(e)})

  finally:
    # Close the database connection and cursor
    cursor.close()
    # db.close()


# Route to fetch categories from the server
@app.route('/get_categories', methods=['GET'])
def get_categories():
    # Fetch categories from the database or any other source 
    try:
        cursor = db.cursor()

        # Fetch categories from the database
        query = 'SELECT id, name FROM category WHERE active = 1'
        cursor.execute(query)
        categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
        cursor.close()
        return jsonify({'categories': categories})
    except mysql.connector.Error as err:
        print(f"Error fetching categories: {err}")
        return jsonify({'error': 'Error fetching categories'})

# Route to add a new item to the menu
@app.route('/add_item', methods=['POST'])
def add_item():
    category = request.form.get('category')
    newCategoryName = request.form.get('newCategoryName')
    itemName = request.form.get('itemName')
    itemPrice = request.form.get('itemPrice')
    itemImage = request.files['itemImage']

    if category != 'newCategory':
        # Add the item to the "item" table
        try:
            # Save the image file to the /static/items folder
            filename = secure_filename(itemImage.filename)
            filepath = os.path.join(app.root_path, 'static', 'items', filename)
            resize_save(itemImage,filepath)
            filepath = '/static/items/'+filename #relative path for image load
            
            # Perform the necessary database operations to insert the item
            # Assuming you have a MySQL connection configured
            cursor = db.cursor()

            # Insert the item details into the "item" table
            query = 'INSERT INTO item (name, category, price, image_path, active) VALUES (%s, %s, %s, %s, %s)'
            values = (itemName, category, itemPrice, filepath, 1)  # Set active to 1 by default
            cursor.execute(query, values)
            db.commit()

            cursor.close()
            return jsonify({'message': 'Item added successfully'})
        except mysql.connector.Error as err:
            print(f"Error adding item: {err}")
            return jsonify({'error': 'Error adding item'})

    else:
        # Handle adding the item to a new category (if desired)
        try:
            # Perform the necessary database operations to add the new category and item
            # Assuming you have a MySQL connection configured
            filename = secure_filename(itemImage.filename)
            filepath = os.path.join(app.root_path, 'static', 'items', filename)
            resize_save(itemImage,filepath)
            filepath = '/static/items/'+filename #relative path for image load
            cursor = db.cursor()

            # Insert the new category into the "category" table
            query = 'INSERT INTO category (name, active) VALUES (%s, %s)'
            values = (newCategoryName, 1)  # Set active to 1 by default
            cursor.execute(query, values)
           

            # Get the newly inserted category ID
            categoryID = cursor.lastrowid

            # Insert the item details into the "item" table with the new category ID
            query = 'INSERT INTO item (name, category, price, image_path, active) VALUES (%s, %s, %s, %s, %s)'
            values = (itemName, categoryID, itemPrice, filepath, 1)  # Set active to 1 by default
            cursor.execute(query, values)
            db.commit()

            cursor.close()
            return jsonify({'message': 'Item added successfully'})
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error adding item with new category: {err}")
            return jsonify({'error': 'Error adding item with new category'})
        


@app.route('/delete_category', methods=['POST'])
def delete_category():
    category_id = request.form.get('categoryId')

    try:
        cursor = db.cursor()

        # We say we delete but we never delete
        update_category_query = f"UPDATE category SET active = 0 WHERE id = {category_id}"
        cursor.execute(update_category_query)

        db.commit()
        cursor.close()

        return jsonify({'message': 'Category deleted successfully'})
    except mysql.connector.Error as err:
        print(f"Error deleting category: {err}")
        return jsonify({'error': 'Error deleting category'})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get('itemId')

    try:
        cursor = db.cursor()

        # We say we delete but we never delete
        update_item_query = f"UPDATE item SET active = 0 WHERE id = {item_id}"

        cursor.execute(update_item_query)

        db.commit()
        cursor.close()

        return jsonify({'message': 'Item deleted successfully'})
    except mysql.connector.Error as err:
        print(f"Error deleting item: {err}")
        return jsonify({'error': 'Error deleting item'})

def convert_GMT_to_IST(gmt_time_str):
    # Convert the GMT time string to a datetime object
    gmt_time = gmt_time_str  # Assuming row[1] contains the GMT datetime object

    # Define the time difference between GMT and IST (5 hours and 30 minutes)
    time_diff = timedelta(hours=5, minutes=30)

    # Convert GMT time to IST by adding the time difference
    ist_time = gmt_time + time_diff

    # Convert IST time back to a formatted string
    ist_time_str = ist_time.strftime("%Y-%m-%d %H:%M:%S")

    return ist_time_str



def resize_save(itemImage, filepath):
    # Open the image using PIL
    image = Image.open(itemImage)

    # Resize the image to 150x150 pixels
    resized_image = image.resize((150, 150))

    # Determine the file extension (jpg or png)
    file_extension = os.path.splitext(filepath)[1].lower()

    # Save the resized image in the appropriate format
    if file_extension == '.jpg' or file_extension == '.jpeg':
        resized_image.save(filepath, 'JPEG')
    elif file_extension == '.png':
        resized_image.save(filepath, 'PNG')

# API Endpoint to fetch orders [REDUNDANT]
@app.route('/api/orders')
def get_orders():
    try:
        cursor = db.cursor()

        query = 'SELECT id, order_time FROM `order`'
        cursor.execute(query)
                # categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

        orders = [{'id': row[0], 'order_time': convert_GMT_to_IST(row[1])} for row in cursor.fetchall()]

        cursor.close()

        return jsonify(orders)
    except mysql.connector.Error as err:
        print(f"Error fetching orders: {err}")
        return jsonify({'error': 'Error fetching orders'}), 500

# API Endpoint to fetch items for a specific order
@app.route('/api/orders/<int:order_id>/items')
def get_order_items(order_id):
    try:
        
        cursor = db.cursor()

        query = '''
            SELECT i.id, i.name, i.price
            FROM order_item oi
            JOIN item i ON oi.item_id = i.id
            WHERE oi.order_id = %s
        '''
        cursor.execute(query, (order_id,))
        items = [{'id': row[0], 'name': row[1], 'price': row[2]} for row in cursor.fetchall()]

        cursor.close()

        return jsonify(items)
    except mysql.connector.Error as err:
        print(f"Error fetching items for order {order_id}: {err}")
        return jsonify({'error': f'Error fetching items for order {order_id}'}), 500

@app.route('/api/order')        
def get_order():
    try:
        cursor = db.cursor()

        query = '''
        SELECT o.id AS order_id, o.order_time, oi.item_id, i.name AS item_name, i.price AS item_price 
        FROM `order` o 
        JOIN order_item oi ON o.id = oi.order_id 
        JOIN item i ON oi.item_id = i.id 
        WHERE o.order_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) 
        ORDER BY o.id DESC;
        '''
        cursor.execute(query)

        orders = {}
        for row in cursor.fetchall():
            order_id = row[0]
            order_time = convert_GMT_to_IST(row[1])
            item_id = row[2]
            item_name = row[3]
            item_price = row[4]

            if order_id not in orders:
                orders[order_id] = {
                    'order_id': order_id,
                    'order_time': order_time,
                    'items': [{'item_id': item_id, 'item_name': item_name, 'item_price': item_price}]
                }
            else:
                orders[order_id]['items'].append({'item_id': item_id, 'item_name': item_name, 'item_price': item_price})

        cursor.close()

        return jsonify(list(orders.values()))
    except mysql.connector.Error as err:
        print(f"Error fetching orders: {err}")
        return jsonify({'error': 'Error fetching orders'}), 500


# Route to fetch expense categories
@app.route('/api/expense_categories', methods=['GET'])
def get_expense_categories():
    try:
      
        cursor = db.cursor()

        query = 'SELECT * FROM `expense_category`'
        cursor.execute(query)

        categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

        cursor.close()

        return jsonify(categories), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

# Route to add an expense
@app.route('/api/add_expense', methods=['POST'])
def add_expense():
    try:
        
        cursor = db.cursor()

        category_id = request.form['expenseCategory']
        value = request.form['expenseValue']
        description = request.form['expenseDescription']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO expense (time, expense_category_id, value, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (timestamp, category_id, value, description))
        db.commit()

        cursor.close()
       

        return jsonify({'message': 'Expense added successfully'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    try:
        cursor = db.cursor()
        query = '''
        SELECT e.id, e.time, ec.name AS category, e.value, e.description
        FROM expense e
        JOIN expense_category ec ON e.expense_category_id = ec.id WHERE active = 1
        ORDER BY e.time DESC
        '''
        cursor.execute(query)

        expenses = []
        for row in cursor.fetchall():
            expense = {
                'id': row[0],
                'time': convert_GMT_to_IST(row[1]),
                'category': row[2],
                'value': row[3],
                'description': row[4]
            }
            expenses.append(expense)

        cursor.close()

        return jsonify({'expenses': expenses})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/api/delete_expense', methods=['POST'])
def delete_expense():
    expense_id = request.form.get('expenseId')
    try:
        # Connect to the database
        cursor = db.cursor()

        # Update the active column of the expense with given expense ID
        update_query = f"UPDATE expense SET active = 0 WHERE id = {expense_id}"
        cursor.execute(update_query)
        db.commit()

        # Close the database connection
        cursor.close()

        return jsonify(message='Expense deleted successfully')
    except mysql.connector.Error as error:
        return jsonify(error=str(error)), 500



if __name__ == '__main__':
    app.run()

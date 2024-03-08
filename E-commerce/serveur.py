from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Chemin vers le fichier JSON qui stocke les données des produits
PRODUCTS_FILE = 'products.json'

def read_products():
    try:
        with open(PRODUCTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_products(products):
    with open(PRODUCTS_FILE, 'w') as file:
        json.dump(products, file, indent=4)

@app.route('/products', methods=['GET'])
def get_products():
    products = read_products()
    category = request.args.get('category')
    in_stock = request.args.get('inStock')

    if category and in_stock in ["True", "true", True, 1] :
        products = [product for product in products if product.get('category') == category and product.get('quantity') > 0 ]

    elif category :
        products = [product for product in products if product.get('category') == category]

    elif in_stock in ["True", "true", True, 1]  :
        products = [product for product in products if product.get('quantity') > 0]

    return jsonify(products)

@app.route('/products/<string:id>', methods=['GET'])
def get_product(id):

    id_int = int(id)

    products = read_products()
    product = next((product for product in products if product['id'] == id_int), None)
    return jsonify(product) if product else ('', 404)

@app.route('/products', methods=['POST'])
def add_product():
    products = read_products()

    list_id = [ product["id"] for product in products ]

    new_id = max(list_id)+1

    product_data = request.json
    product_data['id'] = new_id
    products.append(product_data)
    write_products(products)
    return jsonify(product_data), 201

@app.route('/products/<string:id>', methods=['PUT'])
def update_product(id):

    id_int = int(id)

    products = read_products()
    product = next((product for product in products if product['id'] == id_int), None)
    if not product:
        return ('', 404)
    
    product_update = request.json
    for key, value in product_update.items():
        product[key] = value
    
    write_products(products)
    return jsonify(product)

@app.route('/products/<string:id>', methods=['DELETE'])
def delete_product(id):

    id_int = int(id)

    products = read_products()
    product_index = next((i for i, product in enumerate(products) if product['id'] == id_int), None)
    if product_index is None:
        return ('', 404)
    
    del products[product_index]
    write_products(products)
    return jsonify({'message': 'Product deleted successfully'})








from datetime import datetime

ORDERS_FILE = 'orders.json'

def read_orders():
    try:
        with open(ORDERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_orders(orders):
    with open(ORDERS_FILE, 'w') as file:
        json.dump(orders, file, indent=4)

@app.route('/orders', methods=['POST'])
def create_order():
    orders = read_orders()
    order_data = request.json
    products = read_products()
    
    # Calcul du prix total et vérification de l'existence des produits
    total_price = 0
    for item in order_data['products']:
        product = next((product for product in products if product['id'] == int(item['productId'])), None)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        total_price += product['price'] * int(item.get('quantity', 1))


    list_id = [ order["id"] for order in orders ]

    new_id = max(list_id)+1
    
    order_data['id'] = new_id
    order_data['totalPrice'] = total_price
    order_data['orderStatus'] = 'Pending'
    order_data['orderDate'] = datetime.now().isoformat()
    orders.append(order_data)
    
    write_orders(orders)
    return jsonify(order_data), 201

@app.route('/orders/<string:userId>', methods=['GET'])
def get_orders_by_user(userId):
    orders = read_orders()
    user_orders = [order for order in orders if order.get('userId') == userId]
    return jsonify(user_orders)






CARTS_FILE = 'carts.json'

def read_carts():
    try:
        with open(CARTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_carts(carts):
    with open(CARTS_FILE, 'w') as file:
        json.dump(carts, file, indent=4)

@app.route('/cart/<string:userId>', methods=['POST'])
def add_to_cart(userId):
    carts = read_carts()
    products = read_products()
    
    product_details = request.json
    productId = int(product_details['productId'])
    quantity = int(product_details['quantity'])


    list_id = [ product["id"] for product in products ]

    if int(productId) not in list_id :
        return jsonify({'error': 'Product not found'}), 404

    if userId not in carts:
        carts[userId] = []


    # Check if product already exists in cart
    existing_product = next((item for item in carts[userId] if item['productId'] == productId), None)
    if existing_product:
        existing_product['quantity'] += quantity
    else:
        carts[userId].append(product_details)

    write_carts(carts)
    return jsonify(carts[userId])

@app.route('/cart/<string:userId>', methods=['GET'])
def get_cart(userId):
    carts = read_carts()
    products = read_products()

    user_cart = carts.get(userId, [])

    price = 0
    for product in user_cart :
        for prod in products :
            if int(product["productId"]) == prod["id"]:
                price = price + int(product["quantity"])*int(prod["price"])

    resp = { "cart" : user_cart, "price" : price }

    return jsonify(resp)

@app.route('/cart/<string:userId>/item/<string:productId>', methods=['DELETE'])
def remove_from_cart(userId, productId):
    carts = read_carts()
    if userId in carts:
        carts[userId] = [item for item in carts[userId] if item['productId'] != productId]
        write_carts(carts)
        return jsonify(carts[userId])
    return jsonify({"error": "User or product not found"}), 404








if __name__ == '__main__':
    app.run(debug=True)

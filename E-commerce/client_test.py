import requests

BASE_URL = "http://127.0.0.1:5000"  # Assurez-vous que cette URL correspond à l'URL de votre serveur Flask

def test_get_products_with_filters():
    print("Testing GET /products with filters")

    # Test sans filtres
    print("\nTesting without filters:")
    response = requests.get(f"{BASE_URL}/products")
    print(response.json())

    # Test avec filtre de catégorie
    category_filter = "Category 2"
    print(f"\nTesting with category filter: {category_filter}")
    response = requests.get(f"{BASE_URL}/products", params={"category": category_filter})
    print(response.json())

    # Test avec filtre de stock (inStock = True)
    print("\nTesting with inStock filter: True")
    response = requests.get(f"{BASE_URL}/products", params={"inStock": "true"})
    print(response.json())

    # Test avec filtre de stock (inStock = False)
    print("\nTesting with inStock filter: False")
    response = requests.get(f"{BASE_URL}/products", params={"inStock": "false"})
    print(response.json())

    print("\nTesting with inStock and category")
    response = requests.get(f"{BASE_URL}/products", params={"category": "Category 1", "inStock": "true"})
    print(response.json())


def test_get_product(product_id):

    s = str(product_id)

    print(f"Testing GET /products/{s}")
    response = requests.get(f"{BASE_URL}/products/{s}")
    print(response.json())

def test_add_product():
    print("Testing POST /products")
    new_product = {
        "name": "New Product",
        "description": "Description of new product",
        "price": 150,
        "category": "Category 2",
        "quantity": 12
    }
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    print(response.json())

def test_update_product(product_id):

    s = str(product_id)

    print(f"Testing PUT /products/{s}")
    updated_product = {
        "price": 5000,
        "quantity": 300
    }
    response = requests.put(f"{BASE_URL}/products/{s}", json=updated_product)
    print(response.json())

def test_delete_product(product_id):

    s = str(product_id)

    print(f"Testing DELETE /products/{s}")
    response = requests.delete(f"{BASE_URL}/products/{s}")
    print(response.json())


def test_create_order():
    print("Testing POST /orders")
    new_order = {
        "userId": "user123",
        "products": [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 1}
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=new_order)
    print(response.json())

def test_get_user_orders(user_id):
    print(f"Testing GET /orders/{user_id}")
    response = requests.get(f"{BASE_URL}/orders/{user_id}")
    print(response.json())






def test_add_to_cart(userId, productId, quantity):

    s = str(productId)

    print(f"Testing POST /cart/{userId} for adding product")
    cart_item = {
        "productId": s,
        "quantity": quantity
    }
    response = requests.post(f"{BASE_URL}/cart/{userId}", json=cart_item)
    print(response.json())

def test_get_cart(userId):
    print(f"Testing GET /cart/{userId} to retrieve cart")
    response = requests.get(f"{BASE_URL}/cart/{userId}")
    print(response.json())

def test_remove_from_cart(userId, productId):

    s = str(productId)

    print(f"Testing DELETE /cart/{userId}/item/{s} to remove product from cart")
    response = requests.delete(f"{BASE_URL}/cart/{userId}/item/{s}")
    print(response.json())







if __name__ == "__main__":

    test_get_products_with_filters() # OK

    #test_add_product()  # OK

    #test_get_product(2) # OK

    #test_update_product(2) # OK

    #test_delete_product(2) # OK

    #test_create_order()  # OK

    #test_get_user_orders("user123") # OK

    #test_add_to_cart("user123", 1, 2) # OK
    
    #test_get_cart("user123") # OK
    
    #test_remove_from_cart("user123", 1) # OK


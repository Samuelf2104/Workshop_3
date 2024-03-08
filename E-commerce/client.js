function getProducts(category, inStock) {
  const url = new URL(`${BASE_URL}/products`);
  if (category) url.searchParams.append('category', category);
  if (inStock !== undefined) url.searchParams.append('inStock', inStock);

  return fetch(url)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

function getProduct(id) {
  return fetch(`${BASE_URL}/products/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Product not found');
      }
      return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}


function addProduct(productData) {
  return fetch(`${BASE_URL}/products`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData),
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
}


function updateProduct(id, productData) {
  return fetch(`${BASE_URL}/products/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData),
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
}


function deleteProduct(id) {
  return fetch(`${BASE_URL}/products/${id}`, {
    method: 'DELETE',
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
}




function createOrder(orderData) {
  return fetch(`${BASE_URL}/orders`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(orderData),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Test POST /orders', data);
    return data; // Renvoie les données pour une utilisation ultérieure si nécessaire
  })
  .catch(error => console.error('Error:', error));
}

function getUserOrders(userId) {
  return fetch(`${BASE_URL}/orders/${userId}`)
    .then(response => response.json())
    .then(data => {
      console.log(`Test GET /orders/${userId}`, data);
      return data; // Renvoie les données pour une utilisation ultérieure si nécessaire
    })
    .catch(error => console.error('Error:', error));
}





function addToCart(userId, productId, quantity) {
  const url = `${BASE_URL}/cart/${userId}`;
  const cartItem = {
    productId: String(productId), // Convertir en chaîne de caractères si nécessaire
    quantity: quantity,
  };

  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(cartItem),
  })
  .then(response => response.json())
  .then(data => console.log('addToCart Response:', data))
  .catch(error => console.error('Error:', error));
}

function getCart(userId) {
  const url = `${BASE_URL}/cart/${userId}`;

  return fetch(url)
    .then(response => response.json())
    .then(data => console.log('getCart Response:', data))
    .catch(error => console.error('Error:', error));
}

function removeFromCart(userId, productId) {
  const url = `${BASE_URL}/cart/${userId}/item/${String(productId)}`; // Convertir productId en chaîne de caractères si nécessaire

  return fetch(url, {
    method: 'DELETE',
  })
  .then(response => response.json())
  .then(data => console.log('removeFromCart Response:', data))
  .catch(error => console.error('Error:', error));
}






const BASE_URL = "http://127.0.0.1:5000";


// Test: Obtenir des produits
getProducts('Category 2', true)

// Test: Obtenir un produit spécifique
// Assurez-vous de remplacer '1' par un ID de produit valide dans votre base de données
getProduct(1)

// Test: Ajouter un produit
// Remplacer les valeurs d'example par des valeurs valides pour votre modèle de produit
addProduct({
  name: 'Nouveau produit',
  category: 'electronique',
  price: 199.99,
  quantity: 10
})

// Test: Mettre à jour un produit
// Assurez-vous de remplacer '2' par un ID de produit valide et d'ajuster les données du produit
updateProduct(2, {
  name: 'Produit mis a jour',
  price: 299.99
})

// Test: Supprimer un produit
// Assurez-vous de remplacer '3' par un ID de produit valide
deleteProduct(6)





// Test: Créer une commande
const newOrder = {
  userId: "bonjour",
  products: [
    {productId: 1, quantity: 2},
    {productId: 2, quantity: 1}
  ]
};

createOrder(newOrder);

// Test: Obtenir les commandes d'un utilisateur
const userId = "bonjour";

getUserOrders(userId);






const testUserId = 'salutsalut';
const testProductId = 1;
const testQuantity = 4;

addToCart(testUserId, testProductId, testQuantity)

getCart(testUserId)

removeFromCart(testUserId, testProductId)



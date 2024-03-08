const apiBaseUrl = 'http://localhost:3000'; // Adjust this URL to your server

// Fetch and display products
function fetchProducts() {
    fetch(`${apiBaseUrl}/products`)
        .then(response => response.json())
        .then(products => {
            const productListEl = document.getElementById('product-list');
            products.forEach(product => {
                const productEl = document.createElement('div');
                productEl.className = 'col-md-4';
                productEl.innerHTML = `
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">${product.description}</p>
                            <p class="card-text">Price: $${product.price}</p>
                        </div>
                    </div>
                `;
                productListEl.appendChild(productEl);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
}

document.addEventListener('DOMContentLoaded', fetchProducts);

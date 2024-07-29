import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def update_product(product_id, updates):
    url = f'{BASE_URL}/products/{product_id}.json'
    
    # Only include fields that need to be updated
    product_data = {'product': updates}
    
    response = requests.put(url, headers=HEADERS, json=product_data)
    response.raise_for_status()
    return response.json()



# Example Usage
product_id = '123456789'  # Replace with actual product ID (product id example is 'gid://shopify/Product/123456789')

product_updates = {
    'title': 'New Product Title',
    'status': 'active',  # Can be 'active', 'draft', or 'archived'
    'body_html': '<strong>New product description</strong>',  # Example of updating the product description
}

# Update product attributes
updated_product = update_product(product_id, product_updates)
print("Updated Product:", updated_product)
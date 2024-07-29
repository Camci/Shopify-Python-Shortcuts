import requests

# Replace with your Shopify store URL, API key, and password
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def create_product_rest(title, description, variants):
    url = f"{BASE_URL}/products.json"
    product_data = {
        "product": {
            "title": title,
            "body_html": description,
            "variants": [{"price": variant['price'], "sku": variant['sku']} for variant in variants]
        }
    }

    response = requests.post(url, json=product_data, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data

# Example usage
title = "Example Product"
description = "<strong>Great product</strong> description here."
variants = [
    {"price": "19.99", "sku": "EX-123"},
    {"price": "29.99", "sku": "EX-124"}
]

created_product = create_product_rest(title, description, variants)
print(created_product)

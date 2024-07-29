import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}
def update_variant(variant_id, updates):
    url = f'{BASE_URL}/variants/{variant_id}.json'
    
    # Only include fields that need to be updated
    variant_data = {'variant': updates}
    
    response = requests.put(url, headers=HEADERS, json=variant_data)
    response.raise_for_status()
    return response.json()

# Example Usage
variant_id = '987654321'  # Replace with actual variant ID

variant_updates = {
    'price': '19.99',
    'inventory_quantity': 100,
    'sku': 'NEW-SKU-1234',
    'inventory_policy': 'continue',  # Can be 'deny' or 'continue'
}

# Update variant attributes
updated_variant = update_variant(variant_id, variant_updates)
print("Updated Variant:", updated_variant)

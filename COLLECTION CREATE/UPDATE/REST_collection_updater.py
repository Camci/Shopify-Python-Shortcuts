import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

# Base URL for Shopify REST API
BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07'

def update_collection_title_rest(collection_id, new_title):
    url = f"{BASE_URL}/custom_collections/{collection_id}.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        "custom_collection": {
            "id": collection_id,
            "title": new_title
        }
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Example Usage
collection_id = '1234567890'  # Replace with your collection ID
new_title = "Updated Collection Title"
updated_collection = update_collection_title_rest(collection_id, new_title)
print("Updated Collection (REST):", updated_collection)

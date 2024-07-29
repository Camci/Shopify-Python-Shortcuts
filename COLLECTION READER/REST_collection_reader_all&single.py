import requests

ACCESS_TOKEN = 'YOUR_ADMIN_API_TOKEN'
SHOP_NAME = 'your_shop_name'

def get_all_collections_rest():
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/custom_collections.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    all_collections = []
    params = {'limit': 250}  # Set limit to the max per page

    while url:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_collections.extend(data['custom_collections'])
        url = response.links.get('next', {}).get('url')
        params = None  # No need for params after the first page

    return all_collections

def get_single_collection_rest(collection_id):
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/custom_collections/{collection_id}.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    response = requests.get(url, headers=headers)
    return response.json()['custom_collection']

collection_id = 'YOUR_COLLECTION_ID'
collection = get_single_collection_rest(collection_id)
print(collection)



collections = get_all_collections_rest()
for collection in collections:
    print(collection['id'], collection['title'])

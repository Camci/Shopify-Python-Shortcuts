import requests

# Replace with your Shopify store URL, API key, and password
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def fetch_all_products_rest():
    all_products = []
    endpoint = '/products.json'
    params = {'limit': 250}  # Shopify allows max 250 products per request

    while endpoint:
        response = requests.get(BASE_URL + endpoint, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        all_products.extend(data['products'])
        endpoint = None
        
        if 'link' in response.headers:
            links = response.headers['link'].split(',')
            for link in links:
                if 'rel="next"' in link:
                    # Extract the URL for the next page
                    endpoint = link[link.find('<') + 1:link.find('>')].replace(BASE_URL, '')
                    break

    return all_products


def fetch_single_product_rest(product_id):
    endpoint = f'/products/{product_id}.json'
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data['product']

product_id = 1234567890  # Replace with your actual product ID
product = fetch_single_product_rest(product_id)
print(product)




all_products = fetch_all_products_rest()
for product in all_products:
    print(product['title'], [variant['title'] for variant in product['variants']])
import requests

# Replace these with your own Shopify store details
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

GRAPHQL_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2024-07/graphql.json'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': ACCESS_TOKEN
}

def fetch_all_products_graphql():
    query = """
    query getProducts($first: Int!, $after: String) {
        products(first: $first, after: $after) {
            edges {
                node {
                    id
                    title
                    variants(first: 100) {
                        edges {
                            node {
                                id
                                title
                                sku
                                price
                            }
                        }
                    }
                }
                cursor
            }
            pageInfo {
                hasNextPage
            }
        }
    }
    """
    
    variables = {
        "first": 50,
        "after": None
    }

    all_products = []
    has_next_page = True

    while has_next_page:
        response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        print(data)
        products = data['data']['products']['edges']
        all_products.extend(products)
        
        has_next_page = data['data']['products']['pageInfo']['hasNextPage']
        if has_next_page:
            variables['after'] = products[-1]['cursor']

    return all_products


def fetch_single_product_graphql(product_id):
    query = """
    query getProduct($id: ID!) {
        product(id: $id) {
            id
            title
            variants(first: 50) {
                edges {
                    node {
                        id
                        title
                        price
                    }
                }
            }
        }
    }
    """
    
    variables = {
        "id": product_id
    }

    response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data['data']['product']

product_id = "gid://shopify/Product/1234567890"  # Replace with your actual product ID
product = fetch_single_product_graphql(product_id)
print(product)


all_products = fetch_all_products_graphql()
for product_edge in all_products:
    product = product_edge['node']
    print(product['title'], [variant['node']['title'] for variant in product['variants']['edges']])

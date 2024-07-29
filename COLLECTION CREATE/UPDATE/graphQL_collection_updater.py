import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

# Base URL for Shopify GraphQL API
BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07/graphql.json'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
}

def update_collection_title_graphql(collection_id, new_title):
    # Construct the GraphQL mutation
    mutation = """
    mutation {
        collectionUpdate(input: {
            id: "gid://shopify/Collection/%s",
            title: "%s"
        }) {
            collection {
                id
                title
            }
            userErrors {
                field
                message
            }
        }
    }
    """ % (collection_id, new_title)

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    response.raise_for_status()
    return response.json()

# Example Usage
collection_id = '1234567890'  # Replace with your collection ID
new_title = "Updated Collection Title"
updated_collection = update_collection_title_graphql(collection_id, new_title)
print("Updated Collection (GraphQL):", updated_collection)

import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07/graphql.json'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def update_product_graphql(product_id, title=None, status=None):
    # Construct the GraphQL mutation
    mutation = """
    mutation {
        productUpdate(input: {
            id: "gid://shopify/Product/%s"
            %s
            %s
        }) {
            product {
                id
                title
                status
            }
            userErrors {
                field
                message
            }
        }
    }
    """ % (
        product_id,
        f'title: "{title}"' if title else "",
        f'status: {status}' if status else ""
    )

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    response.raise_for_status()
    return response.json()

# Example Usage
product_id = 'gid://shopify/Product/123456789'  # Replace with actual product ID
# Update product attributes
updated_product = update_product_graphql(
    product_id,
    title="New Product Title",
    status="ACTIVE"  # Can be 'ACTIVE', 'ARCHIVED', or 'DRAFT'
)
print("Updated Product:", updated_product)

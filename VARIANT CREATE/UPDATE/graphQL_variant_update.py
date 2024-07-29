import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'


BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-07/graphql.json'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def update_variant_graphql(variant_id, price=None, inventory_quantity=None, sku=None, inventory_policy=None):
    # Construct the GraphQL mutation
    mutation = """
    mutation {
        productVariantUpdate(input: {
            id: "gid://shopify/ProductVariant/%s"
            %s
            %s
            %s
            %s
        }) {
            productVariant {
                id
                price
                sku
                inventoryPolicy
                inventoryQuantity
            }
            userErrors {
                field
                message
            }
        }
    }
    """ % (
        variant_id,
        f'price: "{price}"' if price else "",
        f'sku: "{sku}"' if sku else "",
        f'inventoryPolicy: {inventory_policy}' if inventory_policy else "",
        f'inventoryQuantity: {inventory_quantity}' if inventory_quantity else ""
    )

    response = requests.post(BASE_URL, headers=HEADERS, json={'query': mutation})
    response.raise_for_status()
    return response.json()

# Example Usage
variant_id = 'gid://shopify/ProductVariant/987654321'  # Replace with actual variant ID

# Update variant attributes
updated_variant = update_variant_graphql(
    variant_id,
    price="19.99",
    inventory_quantity=100,
    sku="NEW-SKU-1234",
    inventory_policy="CONTINUE"  # Can be 'DENY' or 'CONTINUE'
)
print("Updated Variant:", updated_variant)

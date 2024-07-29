#NOTE: IF YOU DO NOT WANT TO CREATE VARIANTS, DON'T ADD AS INPUTS

import requests

# Replace these with your own Shopify store details
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

GRAPHQL_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2024-07/graphql.json'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': ACCESS_TOKEN
}

def create_product_graphql(title, description, variants):
    mutation = """
    mutation createProduct($input: ProductInput!) {
        productCreate(input: $input) {
            product {
                id
                title
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    
    variables = {
        "input": {
            "title": title,
            "bodyHtml": description,
            "variants": [{"price": variant['price'], "sku": variant['sku']} for variant in variants]
        }
    }

    response = requests.post(GRAPHQL_URL, json={'query': mutation, 'variables': variables}, headers=HEADERS)
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

created_product = create_product_graphql(title, description, variants)
print(created_product)

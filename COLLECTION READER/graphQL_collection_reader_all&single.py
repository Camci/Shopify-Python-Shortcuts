import requests

ACCESS_TOKEN = 'YOUR_ADMIN_API_TOKEN'
SHOP_NAME = 'your_shop_name'


def get_all_collections_graphql():
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/graphql.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    all_collections = []
    query = """
    {
      collections(first: 50) {
        edges {
          node {
            id
            title
          }
          cursor
        }
        pageInfo {
          hasNextPage
        }
      }
    }
    """
    variables = {}
    has_next_page = True
    while has_next_page:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        data = response.json()['data']['collections']
        all_collections.extend([edge['node'] for edge in data['edges']])
        has_next_page = data['pageInfo']['hasNextPage']
        if has_next_page:
            cursor = data['edges'][-1]['cursor']
            query = """
            {
              collections(first: 50, after: "%s") {
                edges {
                  node {
                    id
                    title
                  }
                  cursor
                }
                pageInfo {
                  hasNextPage
                }
              }
            }
            """ % cursor

    return all_collections


def get_single_collection_graphql(collection_id):
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/graphql.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    query = """
    query ($id: ID!) {
      collection(id: $id) {
        id
        title
        description
      }
    }
    """
    variables = {'id': collection_id}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    return response.json()['data']['collection']

collection_id = 'YOUR_COLLECTION_ID'
collection = get_single_collection_graphql(collection_id)
print(collection)


collections = get_all_collections_graphql()
for collection in collections:
    print(collection['id'], collection['title'])

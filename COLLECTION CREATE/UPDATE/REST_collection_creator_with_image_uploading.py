import requests

# Replace with your private app's Admin API access token and shop name
ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

# Shopify API versions
API_VERSION = '2024-04'

# Shopify API base URL
BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}'


def upload_image_to_shopify(file_path):
    url = f"{BASE_URL}/images.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    image_data = {
        "image": {
            "attachment": open(file_path, "rb").read().encode("base64").decode()
        }
    }
    response = requests.post(url, json=image_data, headers=headers)
    if response.status_code == 201:
        return response.json()['image']['src']
    else:
        print(f"Error uploading image: {response.json()}")
        return None


def create_collection(collection_name, image_src):
    url = f"{BASE_URL}/custom_collections.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    collection_data = {
        "custom_collection": {
            "title": collection_name,
            "image": {
                "src": image_src
            }
        }
    }
    response = requests.post(url, json=collection_data, headers=headers)
    if response.status_code == 201:
        print("Collection created successfully!")
        return response.json()
    else:
        print(f"Error creating collection: {response.json()}")
        return None


# Path to the image file to be uploaded
image_file_path = "YOUR_IMAGE_FILE_PATH.png"
collection_name = "YOUR_COLLECTION_NAME"

# Upload the image and get the image URL
image_src = upload_image_to_shopify(image_file_path)
if image_src:
    print(f"Image uploaded successfully: {image_src}")
    
    # Create the collection with the uploaded image
    created_collection = create_collection(collection_name, image_src)
    print(f"Created Collection: {created_collection}")
else:
    print("Failed to upload image.")

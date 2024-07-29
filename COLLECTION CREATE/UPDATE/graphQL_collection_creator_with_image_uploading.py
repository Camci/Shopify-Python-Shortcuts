# IN THIS CODE WE WILL CREATE COLLECTION WITH IMAGE UPLOADING IN SHOPIFY

# FIRST CREATE STAGED URL AND UPLOAD IMAGE (Basically creates temporary url to upload image)

#optional: Upload your image into files section of your shopify admin panel (create_file)

# AFTER THAT CREATE COLLECTION WITH UPLOADED (STAGED) IMAGE

import os
import glob
import requests

ACCESS_TOKEN = 'ADMIN_API_TOKEN'
SHOP_NAME = 'shop_name'

count = 0
def create_file(file_url):
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/graphql.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    media_query_2 = """
        mutation fileCreate($files: [FileCreateInput!]!) {
            fileCreate(files: $files) {
                files {
                    alt
                    createdAt
                    id
                }
            }
        }
    """
    media_input_2 = {
        "files": [
            {
                "alt": "fallback text for an image",
                "contentType": "IMAGE",
                "originalSource": file_url
            }
        ]
    }

    response = requests.post(url, json={"query": media_query_2, "variables": {"files": media_input_2["files"]}}, headers=headers)
    if response.status_code != 200:
        print(f"Error creating file: {response.json()}")
    else:
        print(f"File created successfully! Response: {response.json()}")

def create_media(file):
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/graphql.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    media_query = """
        mutation GenerateUploadURL($media_input: [StagedUploadInput!]!) {
            stagedUploadsCreate(input: $media_input) {
                stagedTargets {
                    url
                    resourceUrl
                    parameters {
                        name
                        value
                    }
                }
            }
        }
    """
    media_input = [
        {
            "filename": file,
            "mimeType": "image/png",
            "httpMethod": "POST",
            "resource": "IMAGE"
        }
    ]
    
    response = requests.post(url, json={"query": media_query, "variables": {"media_input": media_input}}, headers=headers)
    if response.status_code != 200:
        print(f"Error creating media: {response.json()}")
        return None, None
    else:
        data = response.json()["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        return  data["url"],data["resourceUrl"], data["parameters"]

def upload_to_staged_url(file, url, parameters):
    with open(file, 'rb') as f:
        files = {param["name"]: (None, param["value"]) for param in parameters}
        files['file'] = (file, f, 'image/png')
        response = requests.post(url, files=files)
        print(f"Upload Response: {response.status_code}, {response.text}")
        return response.status_code
    
def create_collection(Collection_Name, main_url):
    url = f"https://{SHOP_NAME}.myshopify.com/admin/api/2024-04/graphql.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    collection_query = """
            mutation CollectionCreate($input: CollectionInput!) {
            collectionCreate(input: $input) {
                userErrors {
                field
                message
                }
                collection {
                id
                title
                image {
                    src
                }
                descriptionHtml
                handle
                sortOrder
                ruleSet {
                    appliedDisjunctively
                    rules {
                    column
                    relation
                    condition
                    }
                }
                }
            }
            }
            """
    collection_input = {
            "input": {
                "title": Collection_Name,
                "sortOrder": "MANUAL",
                "ruleSet": {
                "appliedDisjunctively": False,
                "rules": [
                    {
                        "column": "TITLE",
                        "relation": "CONTAINS",
                        "condition": Collection_Name
                    },
                    {
                        "column": "TITLE",
                        "relation": "CONTAINS",
                        "condition": "YYYYYY"
                    },
                    {
                        "column": "TITLE",
                        "relation": "NOT_CONTAINS",
                        "condition": "XXXXX"
                    }
                ]
            },
                "image": {
                    "src":main_url
                }
            }
        }
    response = requests.post(url, json={"query": collection_query, "variables": collection_input}, headers=headers)
    if response.status_code != 200:
        print(f"Error creating collection: {response.json()}")
    else:
        print(f"Collection created successfully! Response: {response.json()}")


                            
# Add your image file path here and collection name
image_file = "YOUR_ACTUAL_IMAGE.png"
Collection_Name = "YOUR_COLLECTION_NAME"


staged_url, main_url, parameters = create_media(image_file)
if staged_url:
    status = upload_to_staged_url(image_file, staged_url, parameters)
    print(f"Upload Status: {status}")
    if status == 200 or status == 201:
        print("Media uploaded successfully")
    else:
        print(f"Failed to upload media for file: {image_file}")
else:
            print(f"Failed to get staged URL and parameters for file: {image_file}")


create_collection(Collection_Name, main_url)
create_file(main_url)
                


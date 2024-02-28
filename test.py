import requests
import base64
from database_handler import create_user, get_user_by_id, update_user, delete_user, drop_users_table
from tables import User
import time
import database_handler as db_handler

# Define the URL of your Flask endpoint
url = 'https://filter.markopavlovic.repl.co/upload'

# Read the image file as binary

test_images_list=[ 'img_130.jpg', 'img_247.jpg', 'img_393.jpg', 'img_488.jpg', 'img_630.jpg', 'img_814.jpg', 'img_135.jpg', 'img_254.jpg', 'img_397.jpg', 'img_491.jpg', 'img_65.jpg', 'img_822.jpg', 'img_140.jpg', 'img_255.jpg', 'img_407.jpg', 'img_499.jpg', 'img_665.jpg', 'img_827.jpg', 'img_141.jpg', 'img_269.jpg', 'img_408.jpg', 'img_501.jpg', 'img_690.jpg', 'img_828.jpg', 'img_141.png', 'img_278.jpg', 'img_414.jpg', 'img_517.jpg', 'img_701.jpg', 'img_843.jpg', 'img_158.jpg', 'img_300.jpg', 'img_416.jpg', 'img_521.jpg', 'img_726.jpg', 'img_845.jpg', 'img_160.jpg', 'img_352.jpg', 'img_422.jpg', 'img_523.jpg', 'img_727.jpg', 'img_854.jpg', 'img_163.jpg', 'img_356.jpg', 'img_423.jpg', 'img_534.jpg', 'img_72.jpg', 'img_881.jpg', 'img_18.jpg', 'img_367.jpg', 'img_426.jpg', 'img_552.jpg', 'img_733.jpg', 'img_882.jpg', 'img_197.jpg', 'img_372.jpg', 'img_427.jpg', 'img_561.jpg', 'img_741.jpg', 'img_90.jpg', 'img_198.jpg', 'img_381.jpg', 'img_429.jpg', 'img_576.jpg', 'img_743.jpg', 'img_930.jpg', 'img_203.jpg', 'img_389.jpg', 'img_432.jpg', 'img_581.jpg', 'img_770.jpg', 'img_209.jpg', 'img_391.jpg', 'img_445.jpg', 'img_582.jpg', 'img_782.jpg', 'img_230.jpg', 'img_392.jpg', 'img_463.jpg', 'img_607.jpg', 'img_805.jpg']
#test_images_list=[ ]



def test_upload_endpoint():
  url = "https://filter.markopavlovic.repl.co/upload"  # Replace with the actual URL
  access_token = "123454676868"  # Replace with the actual access token

  headers = {'Authorization': access_token}
  for image in test_images_list:
    
    with open("static/img/"+image, 'rb') as image_file:
      image_data = image_file.read()
  
    # Convert the binary image data to base64
    base64_image_data = base64.b64encode(image_data).decode('utf-8')
    
    # Define the metadata as a dictionary
    metadata = {
      "title": image.strip(".jpg"),
      "description": "A sample image with ksaljhdksalk"
    }
    
    # Construct the JSON data
    data = {"image": base64_image_data, "metadata": metadata}
    response = requests.post(url,json=data, headers=headers)
    
    time.sleep(1)
    if response.status_code == 200:
      print("Success:", response.text)
      import json
      data=json.loads(response.text)
      image_id=data["image_id"]
    elif response.status_code == 401:
      print("Unauthorized:", response.text)
      continue
    else:
      print(response.text)
      print("Error:", response.status_code)
      continue
    if not image_id:
      return "No image id"
  
    url = f"https://filter.markopavlovic.repl.co/status/{image_id}"  # Replace with the appropriate URL
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Image URL:", data["image_url"])
        print("Status:", data["status"])
        print("Scan Result:", data["scan_result"])
    elif response.status_code == 404:
        print("Image not found.")
    else:
        print("An error occurred with status code:", response.status_code)

if __name__ == '__main__':
  #drop_users_table()
  # response = requests.post(url, json=data)

  # # Print the response
  # print(response.status_code)
  # print(response)

  # create_user("John", "Doe", "john2@example.com", "password123")
  # input()
  # user_id=create_user("Alice", "Johnson", "alice2@example.com", "password789")
  # input()
  # update_user(user_id, "Alice", "Johnson-Smith", "alice@example.com", "newpassword")
  # delete_user(user_id)
  # input()
  #test_upload_endpoint()
  for image in test_images_list:
    metadata = """{
      "title": image.strip(".jpg"),
      "description": "A sample image with ksaljhdksalk"
    }"""
    scan_results = "none"
    status = "pending"
    db_handler.create_image(1, image, metadata,
                                           scan_results, status)

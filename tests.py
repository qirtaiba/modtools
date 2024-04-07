import requests
import base64
import unittest

folder_path = "images"
server_url = "http://192.168.0.102:7000/"


class TestUpdateOrCreateImage(unittest.TestCase):
    def test_update_image(self):
        url = server_url+'update_or_create_image'
        location2 = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "altitude": 1389  # in meters
        }

        image_id = '89'
        user_id = '13'
        image_url = "desinger_pvc.png"
        photodna_results = None
        hiveai_results=None
        status = 'pending'
        incident_time = '2022-05-01 10:00:00'
        reportee_name = 'John Doe'
        reportee_ip_address = '192.168.1.3'
        username = 'bla_bla'
        location = location2
        email="slepamacka@gmail.com"
        password="markocar123"
        data = {
            'image_id': image_id,
            'Email':email,
            'Password':password,
            'user_id': user_id,
            'image_url': image_url,
            'photodna_results': photodna_results,
            'hiveai_results':hiveai_results,
            'status': status,
            'incident_time': incident_time,
            'reportee_name': reportee_name,
            'reportee_ip_address': reportee_ip_address,
            'username': username,
            'location': location
        }

        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['image_id'], image_id)

    def test_create_image(self):
        url = server_url+'update_or_create_image'
        user_id = 'user123'
        image_url = 'http://example.com/image.jpg'
        reportee_name = 'John Doe'
        reportee_ip_address = '127.0.0.1'
        username = 'johndoe'
        location = 'New York'

        data = {
            'user_id': user_id,
            'image_url': image_url,
            'reportee_name': reportee_name,
            'reportee_ip_address': reportee_ip_address,
            'username': username,
            'location': location
        }

        response = requests.post(url, json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertIsNotNone(response.json()['image_id'])


class TestUpload(unittest.TestCase):
    def test_upload_success(self):
        url = server_url+'upload'
        email="slepamacka@gmail.com"
        password="markocar123"
        reportee_name = 'John Doe'
        reportee_ip_address = '127.0.0.1'
        location = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "altitude": 1389  # in meters
        }
        metadata = {'title': 'image1', 'extension': 'jpg'}
        with open('desinger_naocare.png', 'rb') as image_file:
            base64_image_data = base64.b64encode(image_file.read()).decode('utf-8')
        print(email)
        data = {
            'Email': email,
            'Password': password,
            'image': base64_image_data,
            'metadata': metadata,
            'reportee_name': reportee_name,
            'reportee_ip_address': reportee_ip_address,
            'location': location
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

class TestUpload(unittest.TestCase):
    def test_upload_success(self):
        url = server_url+'/upload'
        email="slepamacka@gmail.com"
        password="markocar123"
        reportee_name = 'John Doe'
        reportee_ip_address = '127.0.0.1'
        location = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "altitude": 1389  # in meters
        }
        metadata = {'title': 'image1', 'extension': 'jpg'}
        with open('desinger_naocare.png', 'rb') as image_file:
            base64_image_data = base64.b64encode(image_file.read()).decode('utf-8')
        print(email)
        data = {
            'Email': email,
            'Password': password,
            'image': base64_image_data,
            'metadata': metadata,
            'reportee_name': reportee_name,
            'reportee_ip_address': reportee_ip_address,
            'location': location
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')


class TestUploadMultipleImages(unittest.TestCase):
    def test_upload_success(self):
        url = '/upload_images'
        email="slepamacka@gmail.com"
        password="markocar123"
        reportee_name = 'John Doe'
        reportee_ip_address = '127.0.0.1'
        location = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "altitude": 1389  # in meters
            }
        with open('desinger_pvc.png', 'rb') as image_file:
            base64_image_data1 = base64.b64encode(image_file.read()).decode('utf-8')
        with open('desinger_naocare.png', 'rb') as image_file:
            base64_image_data2 = base64.b64encode(image_file.read()).decode('utf-8')    
        images = [
            {
                "image": base64_image_data1,
                "metadata": {
                    "title": "desinger_pvc",
                    "extension": "png"
                },
                'reportee_name': reportee_name,
                'reportee_ip_address': reportee_ip_address,
                'location': location
            },
            {
                "image": base64_image_data2,
                "metadata": {
                    "title": "desinger_naocare",
                    "extension": "png"
                },
                'reportee_name': reportee_name,
                'reportee_ip_address': reportee_ip_address,
                'location': location
            }
        ]

        data = {
            "Email": email,
            "Password": password,
            "images": images
        }

        response = requests.post(url, json=data)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.json()
        self.assertIn('images', data)
        self.assertEqual(len(data['images']), 2)

        image_1 = data['images'][0]
        self.assertEqual(image_1['status'], 'success')
        

        image_2 = data['images'][1]
        self.assertEqual(image_2['status'], 'success')


def test_upload_endpoint():
    image_id=89
    url = f"http://192.168.0.102:7000/status/{image_id}"  # Replace with the appropriate URL
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Image URL:", data["image_url"])
        print("Status:", data["status"])
        print("Photodna results:", data["photodna_results"])
        print("Hiveai   results:", data["hiveai_results"])
    elif response.status_code == 404:
        print("Image not found.")
    else:
        print("An error occurred with status code:", response.status_code)

if __name__ == '__main__':
    unittest.main()
    test_upload_endpoint()
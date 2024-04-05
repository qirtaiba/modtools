from notify import email_action
import requests
import os
import json
import socket
import base64
import database_handler as db_handler

def get_server_ip():
    try:
        # Get the hostname of the local machine
        host_name = socket.gethostname()

        # Get the IP address associated with the hostname
        server_ip = socket.gethostbyname(host_name)

        return server_ip

    except Exception as e:
        print(f"Error getting server IP address: {e}")
        return None

class Actions:
    def __init__(self):
        self.actions = {}

    def register_action(self, action_id, action_instance):
        self.actions[action_id] = action_instance

    def perform_action(self, action_id, image_data):
        if action_id in self.actions:
            action_instance = self.actions[action_id]
            return action_instance.perform_action(image_data)
        else:
            return None


class PhotoDNA_report_action:
    def __init__(self, reporter_name, reporter_email): 
        self.reporter_name= reporter_name
        self.reporter_email= reporter_email
        self.organization_name="MODTOOLS"
        self.server_ip = get_server_ip()
      
    def perform_action(self,image_data):
        print('PhotoDNA Action Called!')
        with open('static/img/' + image_data.image_url, "rb") as image_file:
            binary_data = image_file.read()
        base64_encoded = base64.b64encode(binary_data).decode("utf-8")

        # Report Violation
        try:
            response = requests.post(
                url="https://api.microsoftmoderator.com/photodna/v1.0/Report",
                headers={
                    "Content-Type": "application/json",
                    "Ocp-Apim-Subscription-Key": os.environ["PHOTODNA_KEY"],
                    "x-user": os.environ["x-user"], 
                    "x-pwd": os.environ["x-pwd"]    
                },
                data=json.dumps({
                    "OrgName":self.organization_name,
                    "ReporterName":self.reporter_name,
                    "ReporterEmail": self.reporter_email,
                    "IncidentTime": image_data.incident_time, 
                    "ReporteeName": image_data.username, 
                    "ReporteeIPAddress":image_data.ip_address,
                    "ViolationContentCollection": [
                    {
                    "Name":image_data.image_url,
                    "Value":base64_encoded,
                    "Location":{ "Latitude":image_data.latitude, "Longitude":image_data.longitude, "Altitude":image_data.altitude },
                    "UploadIpAddress": self.server_ip,
                    "UploadDateTime": image_data.created_at,
                    }
                    ],
                    "AdditionalMetadata":[{ "Key":"IsTest", "Value": "true"}]
                    })
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

class Email_Action:
    def __init__(self):
        self.action_admin=db_handler.get_admin_user()
    def  perform_action(self,image_data):
         email_action(self.action_admin.email,image_data)


def get_action_manager(reporter_name, reporter_email):
    action_manager = Actions()
    photo_dna_action = PhotoDNA_report_action(reporter_name, reporter_email)
    email_action = Email_Action()
    # "photo_dna" represents id of the action which connects it with specific plugin!
    action_manager.register_action("photo_dna_action", photo_dna_action)
    action_manager.register_action("email_action", email_action)
    return action_manager

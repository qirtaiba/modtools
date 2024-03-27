import requests
import os


def photoDNA_report():
    url = "https://api.microsoftmoderator.com/photodna/v1.0/Report"
    headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Ocp-Apim-Subscription-Key": os.environ["PHOTODNA_KEY"],
    "x-user": os.environ["x-user"],
    "x-pwd": os.environ["x-pwd"]
    }
    data = {
        "OrgName":"TestOrg",
        "ReporterName":"Reporter1",
        "ReporterEmail":"test@example.org",
        "IncidentTime":"9/10/2014 9:08:14 PM",
        "ReporteeName":"Reportee1",
        "ReporteeIPAddress":"127.0.0.1",
        "ViolationContentCollection": [
        {
        "Name":"test.jpg",
        "Value":"Base 64 image string",
        "Location":{ "Latitude":"", "Longitude":"", "Altitude":"" },
        "UploadIpAddress": "192.168.1.100",
        "UploadDateTime": "2023-08-20T15:30:00Z",
        "AdditionalMetadata":[{"Key":"viewedByEsp","Value":"true"}, {"Key":"publiclyAvailable","Value":"true"}, {"Key":"additionalInfo","Value":"this is a test"}]
        }
        ],
        "AdditionalMetadata":[{ "Key":"IsTest", "Value": "true"}]
        }
    response = requests.post(url, headers=headers, json=data)
    
    print(response.text)
    # if scan_result["IsMatch"]:
    #    return True,scan_result
    # else:
    #    return False,scan_result


def photoDNA(image_url):
    url = "https://api.microsoftmoderator.com/photodna/v1.0/Match?enhance=false"
    headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Ocp-Apim-Subscription-Key": os.environ["PHOTODNA_KEY"] 
    }
    data = {
    "DataRepresentation": "URL",
    "Value":   image_url  
    }
    response = requests.post(url, headers=headers, json=data)
    scan_result=response.json()
    print(scan_result)
    if scan_result["IsMatch"]:
       return True,scan_result
    else:
       return False,scan_result






def check_for_bad_classes(json_result, threshold=0.5):
    
  bad_classes = [
      "yes_nsfw",
      "yes_suggestive",
      "yes_female_underwear",
      "yes_male_underwear",
      "yes_sex_toy",
      "yes_female_nudity",
      "yes_male_nudity",
      "yes_female_swimwear",
      "yes_male_shirtless",
      "yes_gun_in_hand",
      "yes_culinary_knife_in_hand",
      "yes_knife_in_hand",
      "yes_pills",
      "yes_smoking",
      "yes_illicit_injectables",
      "yes_kkk",
      "yes_middle_finger",
      "yes_sexual_activity",
      "yes_hanging",
      "yes_noose",
      "yes_realistic_nsfw",
      "yes_animated_corpse",
      "yes_human_corpse",
      "yes_self_harm",
      "yes_drawing",
      "yes_emaciated_body",
      "yes_child_present",
      "yes_sexual_intent",
      "yes_animal_genitalia_and_human",
      "yes_animated_animal_genitalia",
      "yes_gambling",
      "yes_undressed",
      "yes_confederate",
      "yes_animated_alcohol",
      "yes_alcohol",
      "yes_drinking_alcohol",
      "yes_religious_icon",
      "general_nsfw",
      "no_female_underwear",
      "animated_gun",
      "gun_in_hand",
      "gun_not_in_hand",
      "culinary_knife_in_hand",
      "culinary_knife_not_in_hand",
      "knife_in_hand",
      "knife_not_in_hand",
      "a_little_bloody",
      "other_blood",
      "very_bloody",
      "yes_smoking",
      "illicit_injectables",
      "medical_injectables",
      "hanging",
      "animated_corpse",
      "human_corpse", 
      "animal_genitalia_and_human",
      "animal_genitalia_only",
      "animated_animal_genitalia",
      "animated_alcohol",
      "general_suggestive",
  ]
      
  output = json_result.get("status", [])[0].get("response", {}).get("output", [])
  harmful_classes = []
  
  for item in output:
        classes = item.get("classes", [])
        for class_info in classes:
            class_name = class_info.get("class", "")
            score = class_info.get("score", 0)
            
            if class_name in bad_classes and score >= threshold:
                harmful_classes.append(class_name.strip("yes_"))
    
  if harmful_classes:
        return True, ", ".join(harmful_classes)
  else:
        return False, None


def hiveAI_scan_harmfull_content(url):
    payload={"url": url}
    
    headers = {
    "accept": "application/json",
    "authorization": "token {}".format( os.environ["HIVEAI_KEY"] )
    }
    
    response = requests.post("https://api.thehive.ai/api/v2/task/sync", headers=headers, data=payload)
    
    response=response.json()
    
    harmfull_content, bad_class = check_for_bad_classes(response)
    if harmfull_content:
      return True,f"Harmfull content found: {bad_class}"
    else:
      return False,""


if __name__=="__main__":
  image_url="https://s3.amazonaws.com/docs.thehive.ai/client_demo/moderation_image.png"   
  #   photoDNA(image_url)  
  #   print(hiveAI_scan_harmfull_content(image_url))
  #photoDNA_report(image_url)


import requests
import json


def send_request():
    # Report Violation
    # POST https://api.microsoftmoderator.com/photodna/v1.0/Report

    try:
        response = requests.post(
            url="https://api.microsoftmoderator.com/photodna/v1.0/Report",
            headers={
                "Content-Type": "",
                "Ocp-Apim-Subscription-Key": os.environ["PHOTODNA_KEY"],
                "x-user": os.environ["x-user"],
                "x-pwd":  os.environ["x-pwd"] 
            },
            data=json.dumps({
                "OrgName":"TestOrg",
                "ReporterName":"Reporter1",
                "ReporterEmail":"test@example.org",
                "IncidentTime":"9/10/2014 9:08:14 PM",
                "ReporteeName":"Reportee1",
                "ReporteeIPAddress":"127.0.0.1",
                "ViolationContentCollection": [
                {
                "Name":"test.jpg",
                "Value":"Base 64 image string",
                "Location":{ "Latitude":"", "Longitude":"", "Altitude":"" },
                "UploadIpAddress": "192.168.1.100",
                "UploadDateTime": "2023-08-20T15:30:00",
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

send_request()
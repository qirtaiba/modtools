import requests
import os

class PhotoScanApp:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def scan_photo(self, photo_path):
        analysis_results = []
        for plugin in self.plugins:
            analysis = plugin.analyze_photo(photo_path)
            analysis_results.append(analysis)
        return analysis_results

class HiveAI_Plugin:
    def check_for_bad_classes(self, json_result, threshold=0.5):
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
    
    
    def analyze_photo(self,url):
        payload={"url": url}
        
        headers = {
        "accept": "application/json",
        "authorization": "token {}".format( os.environ["HIVEAI_KEY"] )
        }
        
        response = requests.post( "https://api.thehive.ai/api/v2/task/sync", headers=headers, data=payload)
        
        response=response.json()
        
        harmfull_content, bad_class = self.check_for_bad_classes(response)
        if harmfull_content:
          return True,f"Harmfull content found: {bad_class}"
        else:
          return False,""





class PhotoDNA_Plugin:
    def analyze_photo(self,image_url):
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
      if scan_result["IsMatch"]:
         return True,"PhotoDNA match"
      else:
         return False,"No PhotoDNA match"
    

def initialize_photo_scan_app():
  photo_scan_app = PhotoScanApp()
  face_detection_plugin = HiveAI_Plugin()
  object_recognition_plugin = PhotoDNA_Plugin()
  photo_scan_app.register_plugin(face_detection_plugin)
  photo_scan_app.register_plugin(object_recognition_plugin)
  return photo_scan_app

if __name__=="__main__":
  photo_path ="https://s3.amazonaws.com/docs.thehive.ai/client_demo/moderation_image.png"  
  photo_scan_app=initialize_photo_scan_app()
  analysis_results = photo_scan_app.scan_photo(photo_path)
  
  for analysis in analysis_results:
      print(analysis)

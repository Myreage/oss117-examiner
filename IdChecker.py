import requests 
import base64
import json
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class HttpError(Exception):
    def __init__(self, code, reason, request):
        self.code = code
        self.reason = reason
        self.request = request

    def toString(self):
        
        return str(self.code) + " " + self.reason + " : " + self.request


def checkMRZ(image_file):
    
    # Encode image to base64 string
    image_str = base64.b64encode(image_file)
    image_str = image_str.decode("utf-8")

    values = {"file" : image_str}
    r = requests.post(config['DEFAULT']['ApiUrl'] + '/check-document/identities', data=json.dumps(values), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + config['DEFAULT']['ApiToken']})

    print(requests.codes.OK)
    if r.status_code not in [200,201] :       
        raise HttpError(r.status_code, r.reason, r.text)

    result = r.json()

    extracted_fields = {
        "firstName" : result['extractedFirstNames'][0],
        "lastName" : result['extractedBirthName'],    
        "birthDate" : result['extractedBirthDate'],
        "gender" : result['extractedGender'],
        "valid" : result['valid'],
        "expired" : result['expired']

    }
    return extracted_fields
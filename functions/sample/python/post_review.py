import sys
import json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
  
    status_code = 200
    resp = ''
    headers = {'Content-Type':'application/json'}
    
    authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict['COUCH_URL'])
    
    try:
        
        resp = service.post_document(db='reviews', document=dict["review"]).get_result()

    except Exception as err:
        status_code = 500
        resp = str(err)
        
    finally:
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': resp
        }

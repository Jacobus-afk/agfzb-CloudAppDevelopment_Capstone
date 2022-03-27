import sys
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
        resp = service.post_find(
            db='reviews',
            selector={'dealership': {'$eq': int(dict["id"])}},
        ).get_result()
    
        if len(resp['docs']) == 0:
            status_code = 404

    except Exception as err:
        status_code = 500
        resp = str(err)
        
    finally:
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': resp
        }

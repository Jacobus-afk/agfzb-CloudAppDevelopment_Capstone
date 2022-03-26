/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     
    const secret = {
        COUCH_URL: "https://apikey-v2-1zu36jhjj3wlcqelugj4ulumbmorzckdvlbqfbmwvamk:ccaa2118d9eb704bd6c1ac03bc594cdd@d1548402-28e1-4f4a-a948-37ebd76a8d29-bluemix.cloudantnosqldb.appdomain.cloud",
        IAM_API_KEY: "NubmTUUUcpsViZ8RU0li4GzxgXoNMplV0UHILcExvQC5",
        COUCH_USERNAME: "apikey-v2-1zu36jhjj3wlcqelugj4ulumbmorzckdvlbqfbmwvamk"
    };
     
     const cloudant = Cloudant({
         url: secret.COUCH_URL,
         plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
     });
 
    let status_code = 200;
    let headers = { 'Content-Type': 'application/json' };
    let resp = '';
 
    const dealershipDB = await cloudant.use('dealerships');
 
    if (params.state) {
        try {
            let resp = await dealershipDb.find({
                "selector": {
                    "state": {
                        "$eq": params.state
                    }
                }
            });
            
        } catch (error) {
            return { error: error.description } ;
        }
    }
    else {
        try {
            resp =  await cloudant.use('dealerships').list({ include_docs: true });
            
        } catch (error) {
            return { error: error.description } ;
        }
    }
 
    return {
        statusCode: status_code,
        headers: headers,
        body: resp
    }
 }

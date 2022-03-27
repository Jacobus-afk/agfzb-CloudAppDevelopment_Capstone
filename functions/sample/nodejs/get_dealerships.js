/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');
const openwhisk = require('openwhisk');
const ow = openwhisk();

async function main(params) {
     
    const secret = await ow.actions.invoke({ 
        name: 'dealerships/retrieve_credentials',
        blocking: true,
        result: true,
        params: {}
    })
     
    const cloudant = Cloudant({
        url: secret.COUCH_URL,
        plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
    });
    
    let status_code = 200;
    let headers = { 'Content-Type': 'application/json' };
    let resp = '';
    
    if (params.state) {
        try {
            resp = await cloudant.use('dealerships').find({
                "selector": {
                    "st": {
                        "$eq": params.state
                    }
                }
            });
            
            if (resp.docs.length==0) {
                status_code = 404;
            }
            
        } catch (error) {
            resp = error.description;
            status_code = 500
        }
    }

    else {
        try {
            resp =  await cloudant.use('dealerships').list({ include_docs: true });
            
            if (resp.rows.length==0) {
                status_code = 404;
            }
            
        } catch (error) {
            resp = error.description;
            status_code = 500
        }
    }
    
    return {
        statusCode: status_code,
        headers: headers,
        body: resp
    }
}

/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
function main(params) {
    let dealership_list = ''
    try {
        dealership_list = params.body.rows.map((row) => { return {
            id: row.doc.id,
            city: row.doc.city,
            state: row.doc.state,
            st: row.doc.st,
            address: row.doc.address,
            zip: row.doc.zip,
            lat: row.doc.lat,
            long: row.doc.long,
    }});      
    } catch(error) {
        dealership_list = params.body.docs.map((row) => { return {
            id: row.id,
            city: row.city,
            state: row.state,
            st: row.st,
            address: row.address,
            zip: row.zip,
            lat: row.lat,
            long: row.long,
    }});
        
        
    }

    
    return {
        statusCode: params.statusCode,
        headers: params.headers,
        body: dealership_list
    };
}

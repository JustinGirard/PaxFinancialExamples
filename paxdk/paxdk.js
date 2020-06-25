function Paxdk(url_version_in = 'dev',api_key_in='pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a') {
    this.url_version = url_version_in;
    this.api_key = api_key_in;
}

Paxdk.prototype.query = function(query_name,query_in)  {
    url = 'https://g46w1ege85.execute-api.us-west-2.amazonaws.com/alpha/'+this.url_version+'/data/query';
    req = { qtype: query_name, api_key: this.api_key };
    req['__str_encoded_query'] =JSON.stringify(query_in);
    var encodedString = btoa(req['__str_encoded_query']);
    encodedString  = encodeURIComponent(encodedString);
    // ret_dat = {error:'jquery request failed'}
    req['__str_encoded_query'] = encodedString;
    
    return $.ajax({
        type: 'GET',
        url: url,
        data: req,
        success: function (data) {
            console.log('SUCCESS')
        },
        error: function (data) {
            console.log('ERROR')
        }
    })    
}
# restapi
Welcome to homework of Flask based REST API
Supported API:
 - Getting a random word by a GET request to http:/<address>/api/v1.0/random_word
    need authorization, return string
    using public api http://www.setgetgo.com/randomword/
 - Getting a wiki article for word by a GET request to http:/<address>/api/v1.0/wiki/<string:word>
    return unicode of article in WikiText format
    using wiki public api
 - Getting N most popular for word by a GET request to http:/<address>/api/v1.0/wiki/most_popular/<int:N>
    return json with list of most popular
 - Getting joke about Chuck Norris most popular for word by a GET request to http:/<address>/api/v1.0/joke
    if needed provide firstName to replace "Chuck" and lastName to replace "Norris" in joke 
    return string
    using public api http://www.icndb.com/api/
 

# Installation
Python2.7 and enjoy requirements.txt 


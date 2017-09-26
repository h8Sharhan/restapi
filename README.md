# restapi
Welcome to homework of Flask-based REST API:
- Getting a random word by a GET request to "http:/server/api/v1.0/random_word". 
 Need authorization, return string. Use public api http://www.setgetgo.com/randomword/.
 - Getting a wiki article for word by a GET request to "http:/server/api/v1.0/wiki/word", where word is given string. Return unicode of article in WikiText format. Use public wiki api.
 - Getting N most popular submitted to previous operation by a GET request to "http:/server/api/v1.0/wiki/most_popular/N", where N is given integer. Return list of most popular. To save data yaml storage is used.
 - Getting joke about Chuck Norris most popular for word by a GET request to http:/server/api/v1.0/joke, to change "Chuck Norris" by different name pls use parameters firstNameand lastName. Return string. Use public api http://www.icndb.com/api/.
 
# Installation
Python2.7 and apply requirements.txt 

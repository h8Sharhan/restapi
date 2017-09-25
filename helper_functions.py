import json
import logging
import requests


# URLs
RANDOM_WORD_URL = 'http://setgetgo.com//randomword//get.php'
# For details pls visit https://www.mediawiki.org/wiki/API:Main_page
WIKI_URL = 'https://en.wikipedia.org//w//api.php?action=query&titles=%s&prop=revisions&rvprop=content&format=json&' \
           'redirects=1'
CHUCK_NORRIS_JOKE_URL = 'http://api.icndb.com//jokes//random?escape=javascript'

# Simplify method to send get request and handle it exceptions
def _get_request(url):
    try:
        return requests.get(url)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return


# Get random word
def get_random_word():
    response = _get_request(RANDOM_WORD_URL)
    if not response or response.status_code != requests.codes.ok or not response.text:
        return
    return response.text


# Get text of article from wiki
def get_wiki_article(word):
    response = _get_request(WIKI_URL % word)
    if not response or response.status_code != requests.codes.ok:
        return
    # Load json data
    data = json.loads(response.text)
    # Parse data to get text of article
    try:
        page_id = data['query']['pages'].keys()[0]
        text = data['query']['pages'][page_id]['revisions'][0]['*']
    except (KeyError, IndexError):
        return
    # Return unicode string in WikiText format
    return text


# Get joke about Chuck Norris
def get_chuck_norris_joke(first_name=None, last_name=None):
    url = CHUCK_NORRIS_JOKE_URL
    # Prepare url
    if first_name or last_name:
        if first_name:
            url = url + '&firstName=' + first_name
        if last_name:
            url = url + '&lastName=' + last_name
    response = _get_request(url)
    if not response or response.status_code != requests.codes.ok:
        return
    json_data = response.json()
    if json_data['type'] != 'success':
        return
    return json_data['value']['joke']


if __name__ == '__main__':
    print 'Random word: ', get_random_word()
    print 'Wiki article: ', get_wiki_article('Ninja')
    print 'Chuck Norris joke: ', get_chuck_norris_joke()
    print 'Alex Norris joke: ', get_chuck_norris_joke(first_name='Alex')

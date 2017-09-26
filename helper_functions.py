import logging
import requests
from json import loads

import exceptions


# URLs
RANDOM_WORD_URL = 'http://setgetgo.com//randomword//get.php'
# For details pls visit https://www.mediawiki.org/wiki/API:Main_page
WIKI_URL = 'https://en.wikipedia.org//w//api.php?action=query&titles=%s&prop=revisions&rvprop=content&format=json&' \
           'redirects=1'
CHUCK_NORRIS_JOKE_URL = 'http://api.icndb.com//jokes//random?escape=javascript'


logger = logging.getLogger(__name__)


# Simplify method to send get request and handle it exceptions
def _get_request(url):
    try:
        return requests.get(url)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
        logger.warning('Failed connect to %s', url)
        raise exceptions.ExternalApiConnectionError


# Get random word
def get_random_word():
    response = _get_request(RANDOM_WORD_URL)
    if response.status_code != requests.codes.ok or not response.text:
        logger.warning('Failed to get random word code:%s response:%s', response.status_code, response.text)
        raise exceptions.ExternalApiFetchError
    return response.text


# Get text of article from wiki
def get_wiki_article(word):
    response = _get_request(WIKI_URL % word)
    if response.status_code != requests.codes.ok:
        logger.warning('Failed to get wiki article for word:%s code:%s', word, response.status_code)
        raise exceptions.ExternalApiFetchError
    # Load json data
    data = loads(response.text)
    # Parse data to get text of article
    try:
        page_id = data['query']['pages'].keys()[0]
        text = data['query']['pages'][page_id]['revisions'][0]['*']
    except (KeyError, IndexError):
        logger.warning('Failed to parse wiki response data:%s', data)
        raise exceptions.ExternalApiParseError
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
    if response.status_code != requests.codes.ok:
        logger.warning('Failed to get joke, code:%s response:%s', response.status_code, response.text)
        raise exceptions.ExternalApiFetchError
    json_data = response.json()
    if json_data['type'] != 'success':
        logger.warning('Failed to get joke, status:%s', json_data['type'])
        raise exceptions.ExternalApiFetchError
    return json_data['value']['joke']


if __name__ == '__main__':
    print 'Random word: ', get_random_word()
    print 'Wiki article: ', get_wiki_article('Ninja')
    print 'Chuck Norris joke: ', get_chuck_norris_joke()
    print 'Alex Norris joke: ', get_chuck_norris_joke(first_name='Alex')

import requests, json


random_word_url = 'http://setgetgo.com/randomword/get.php'
wiki_url = 'https://en.wikipedia.org/w/api.php'


# GET random word
def get_random_word():
    response = requests.get(random_word_url)
    if response.status_code == 200:
        return response.text


# GET from wiki
def get_wiki_article(word):
    url = wiki_url + "?action=query&prop=revisions&rvprop=content&format=json&redirects=1&titles=%s" % word
    response = requests.get(url)
    # TODO add check of response
    if response.status_code == 200:
        return response.text


if __name__ == '__main__':
    print 'Random word: ', get_random_word()
    print 'Wiki article: ', get_wiki_article('Ninja')

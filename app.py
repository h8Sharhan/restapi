import atexit
import logging
from functools import wraps
from flask import abort, Flask, jsonify, make_response, request


import external_api_exceptions
import helper_functions
from statistic_collection import StatisticCollection


# Dict for user accounts
USERS = {'user': 'qwe123'}


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s: %(message)s",
                    datefmt='%Y.%m.%d %H:%M:%S')

app = Flask('app')


def need_authorization(func):
    wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username not in USERS or auth.password != USERS[auth.username]:
            return abort(make_response('Pls login to use service.', 401))
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    text = """
    Welcome to homework
    Supported RESTfull API:
     - Getting a random word by a GET request to http:/<address>/api/v1.0/random_word
        need authorization, return string
     - Getting a wiki article for word by a GET request to http:/<address>/api/v1.0/wiki/<string:word>
        return unicode of article in WikiText format
     - Getting N most popular for word by a GET request to http:/<address>/api/v1.0/wiki/most_popular/<int:N>
        return json with list of most popular
     - Getting joke about Chuck Norris most popular for word by a GET request to http:/<address>/api/v1.0/joke
        if needed provide firstName to replace "Chuck" and lastName to replace "Norris" in joke 
        return string
    """
    return text


@app.route('/api/v1.0/random_word', methods=['GET'])
@need_authorization
def get_random_word():
    try:
        word = helper_functions.get_random_word()
    except external_api_exceptions.ExternalApiError:
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success', 'result': word})


@app.route('/api/v1.0/wiki/<string:word>', methods=['GET'])
def get_wiki_for_word(word):
    try:
        article = helper_functions.get_wiki_article(word)
    except external_api_exceptions.ExternalApiError:
        return jsonify({'status': 'fail'})
    # Save to collection
    wiki_collection.save(word)
    return jsonify({'status': 'success', 'result': article})


@app.route('/api/v1.0/wiki/most_popular/<int:n>', methods=['GET'])
def get_most_popular(n):
    popular = wiki_collection.get_most_popular(n)
    return jsonify({'status': 'success', 'result': popular})


@app.route('/api/v1.0/joke', methods=['GET'])
def get_joke():
    try:
        joke = helper_functions.get_chuck_norris_joke(request.args.get('firstName'), request.args.get('lastName'))
    except external_api_exceptions.ExternalApiError:
        return jsonify({'status': 'fail'})
    return jsonify({'status': 'success', 'result': joke})


if __name__ == '__main__':
    # Create collection for wiki requests
    wiki_collection = StatisticCollection()
    atexit.register(wiki_collection.save_collection_to_file)
    # Run app
    app.run()
from flask import abort, Flask, jsonify, make_response, request

import helper_functions
from statistic_collection import StatisticCollection


app = Flask(__name__)
wiki_collection = StatisticCollection()
users = {'user': 'qwe123'}


def need_authorization(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username not in users or auth.password != users[auth.username]:
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
     - Getting a wiki article for word by a GET request to http:/<address>/api/v1.0/wiki?search=<word>
        return unicode of article in WikiText format
     - Getting N most popular for word by a GET request to http:/<address>/api/v1.0/wiki/most_popular?N=<integer>
        return json with list of most popular
     - Getting joke about Chuck Norris most popular for word by a GET request to http:/<address>/api/v1.0/chuck_norris
        if needed provide firstName to replace "Chuck" and lastName to replace "Norris" in joke 
        return string
    """
    return text


@app.route('/api/v1.0/random_word', methods=['GET'])
@need_authorization
def get_random_word():
    word = helper_functions.get_random_word()
    if not word:
        abort(make_response('Cannot get random word now. Pls try later.', 404))
    return word


@app.route('/api/v1.0/wiki', methods=['GET'])
def get_wiki_for_word():
    word = request.args.get('search')
    if not word:
        abort(make_response('Pls define "search" parameter', 400))
    article = helper_functions.get_wiki_article(word)
    if not article:
        abort(make_response('Cannot find wiki article for specified word.', 404))
    # Save to collection
    wiki_collection.save(word)
    return article


@app.route('/api/v1.0/wiki/most_popular', methods=['GET'])
def get_most_popular():
    n = request.args.get('N')
    if not n or not n.isdigit():
        abort(make_response('Pls define integer "N" parameter', 400))
    # Get n most popular from collection
    popular = wiki_collection.get_most_popular(int(n))
    # If collection statistic is empty popular will be empty too
    if not popular:
        abort(make_response('Cannot get most popular now. Pls try later.', 404))
    return jsonify(popular)


@app.route('/api/v1.0/chuck_norris', methods=['GET'])
def get_joke():
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    # Get joke
    joke = helper_functions.get_chuck_norris_joke(first_name, last_name)
    if not joke:
        abort(make_response('Cannot get joke now. Pls try later.', 404))
    return joke


if __name__ == '__main__':
    app.run(debug=True)

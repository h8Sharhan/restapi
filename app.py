import json
from flask import abort, Flask, jsonify, request
import helper_functions
from statistic_collection import StatisticCollection


app = Flask(__name__)
wiki_collection = StatisticCollection()


@app.route('/')
def index():
    text = """
    Welcome to homework
    Supported RESTfull API:
     - Getting a random word by a GET request to http:/<address>/api/v1.0/random_word
        return string
     - Getting a wiki article for word by a GET request to http:/<address>/api/v1.0/wiki
        provide word by json data-format {'word': 'Ninja'}
        return unicode of article in WikiText format
     - Getting N most popular for word by a GET request to http:/<address>/api/v1.0/wiki/most_popular
        provide N by json data-format {'N': 3}
        return json with list of most popular
     - Getting joke about Chuck Norris most popular for word by a GET request to http:/<address>/api/v1.0/chuck_norris
        if needed pls provide firstName and lastName by json data-format {"firstName":"John", "lastName":"Pupkin"}
        return string
    """
    return text


@app.route('/api/v1.0/random_word', methods=['GET'])
def get_random_word():
    word = helper_functions.get_random_word()
    if not word:
        abort(400)
    return word


@app.route('/api/v1.0/wiki', methods=['GET'])
def get_wiki_for_word():
    request.get_data()
    try:
        data = json.loads(request.data)
    except ValueError:
        abort(400)
    if not data or 'word' not in data or not isinstance(data.get('word'), unicode):
        abort(400)
    word = data.get('word')
    article = helper_functions.get_wiki_article(word)
    if not article:
        abort(404)
    # Save to collection
    wiki_collection.save(word)
    return article


@app.route('/api/v1.0/wiki/most_popular', methods=['GET'])
def get_most_popular():
    request.get_data()
    try:
        data = json.loads(request.data)
    except ValueError:
        abort(400)
    if not data or 'N' not in data or not isinstance(data.get('N'), int):
        abort(400)
    # Get N most popular from collection
    popular = wiki_collection.get_most_popular(data.get('N'))
    # If collection statistic is empty popular will be empty too
    if not popular:
        abort(400)
    return jsonify(popular)


@app.route('/api/v1.0/chuck_norris', methods=['GET'])
def get_joke():
    request.get_data()
    try:
        data = json.loads(request.data)
    except ValueError:
        abort(400)
    # Get joke
    first_name = None
    last_name = None
    if request.data:
        if 'firstName' in data:
            first_name = data.get('firstName')
        if 'lastName' in data:
            last_name = data.get('lastName')
    joke = helper_functions.get_chuck_norris_joke(first_name, last_name)
    if not joke:
        abort(400)
    return joke


if __name__ == '__main__':
    app.run(debug=True)

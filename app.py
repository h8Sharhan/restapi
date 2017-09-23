from flask import abort, Flask, jsonify, request
from helper_functions import get_random_word, get_wiki_article
from statistic_collection import StatisticCollection


app = Flask(__name__)
wiki_collection = StatisticCollection()
#wiki_collection.collection_dict = {'ninja': 73, 'jedi': 14, 'cruiser': 153, 'destroyer': 25, 'battleship': 73}

@app.route('/')
def index():
    text = """
    Welcome to my homework
    Supported RESTfull API:
     - Getting a random word by a GET request to http:/<address>/api/random_word
     - Getting a wiki article for word by a GET request to http:/<address>/api/wiki
     - Getting N most popular for word by a GET request to http:/<address>/api/most_popular
    """
    return text


@app.route('/api/random_word', methods=['GET'])
def get_random_word():
    word = get_random_word()
    if not word:
        abort(400)
    return word


@app.route('/api/wiki', methods=['GET'])
def get_wiki_for_word():
    if not request.json or 'word' not in request.json or not isinstance(request.json.get('word'), str):
        abort(400)
    # Save to collection
    word = request.json.get('word').lower()
    wiki_collection.save_to_collection(word)
    return jsonify(get_wiki_article(word))


@app.route('/api/most_popular', methods=['GET'])
def get_most_popular():
    if not request.json or 'N' not in request.json or not isinstance(request.json.get('N'), int):
        abort(400)
    # Get n most popular from collection
    popular = wiki_collection.get_most_popular(request.json.get('N'))
    return jsonify(popular)


if __name__ == '__main__':
    app.run(debug=True)

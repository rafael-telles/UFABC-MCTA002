from flask import Flask, escape, request, jsonify
from flask_cors import CORS

from search_trie import Trie
import mmap


with open('trie.data', 'r+') as trie_file:
    buffer = mmap.mmap(trie_file.fileno(), 0)
    trie = Trie(buffer)


def return_closest_words(words):
    suggestions = {}
    for word in words:
        results = trie.search(word)
        results = { value[0].decode('utf-8'):value[1] for value in results }
        if word not in results:
            suggestions[word] = results
        
    return suggestions

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/suggestions', methods=['POST'])
def return_words():
    words = request.json['words']
    closest_words = return_closest_words(words)
    return jsonify(closest_words)

# @app.route('/api/suggestions', methods=['OPTIONS'])
# def suggestion_options():
#    response = jsonify({'some': 'data'})     
#    response.headers.add('Access-Control-Allow-Origin', '*') 
#    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
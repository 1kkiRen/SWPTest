import json
import analyzer

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = {}


@app.route('/api/data/comments', methods=['GET', 'POST'])
def get_comments():
    if request.method == 'POST':
        url = request.form.get('url')
        comments_number = 30
        analyzed_comments = analyzer.analyze_comments(url, comments_number)
        json_data = analyzed_comments.to_json(orient='records', force_ascii=False)
        print(json_data)
        return json_data

    else:
        response = jsonify(data)
        return response


@app.route('/api/data/word_cloud', methods=['GET', 'POST'])
def get_word_cloud():
    if request.method == 'POST':
        url = request.form.get('url')
        comments_number = request.form.get('comments_number')
        word_cloud = analyzer.sentiment_of_most_frequent_words(analyzer.most_frequent_words(url, comments_number))
        json_data = json.dumps(word_cloud)
        print(json_data)

        return json_data

    else:
        response = jsonify(data)
        return response


if __name__ == '__main__':
    app.run()

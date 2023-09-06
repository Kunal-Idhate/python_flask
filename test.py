from flask import Flask, request, jsonify
import requests
import awsgi

app = Flask(__name__)
BASE_URL = 'https://app.ylytic.com/ylytic/test'

@app.route('/search')
def search_comments():
    try:
       
        response = requests.get(BASE_URL)
        data = response.json()
        comments = data['comments']

        search_author = request.args.get('search_author')
        at_from = request.args.get('at_from')
        at_to = request.args.get('at_to')
        like_from = request.args.get('like_from')
        like_to = request.args.get('like_to')
        reply_from = request.args.get('reply_from')
        reply_to = request.args.get('reply_to')
        seach_text = request.args.get('seach_text')

        print(seach_text)
       
        def filter_comments(comment):
            author_matches = not search_author or search_author in comment['author']
            date_matches = (not at_from or comment['at'] >= at_from) and (not at_to or comment['at'] <= at_to)
            like_matches = (not like_from or comment['like'] >= int(like_from)) and (not like_to or comment['like'] <= int(like_to))
            reply_matches = (not reply_from or comment['reply'] >= int(reply_from)) and (not reply_to or comment['reply'] <= int(reply_to))
            text_matches = not seach_text or seach_text in comment['text']

            return  author_matches and date_matches and like_matches and reply_matches and text_matches

        filtered_comments = list(filter(filter_comments, comments))
        return jsonify(filtered_comments)

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# def lambda_handler(event, context):
#     return awsgi.response(app, event, context, base64_content_types={"image/png"})

if __name__ == '__main__':
    app.run(debug=True)

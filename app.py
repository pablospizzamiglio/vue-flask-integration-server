from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import uuid
import sys

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Doctor Sleep',
        'author': 'Stephen King',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Brave New World',
        'author': 'Aldous Huxley',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'The Light of Other Days',
        'author': 'Arthur Clark, Stephen Baxter, Guy Abadia',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'The Island',
        'author': 'Aldous Huxley',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Dearly Devoted Dexter',
        'author': 'Jeff Lindsay',
        'read': False
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

@app.route('/books', methods=['GET'])
def get_all_books():
    response = {
        'status': 'success',
        'books': BOOKS
    }
    return jsonify(response)

@app.route('/books', methods=['POST'])
def post_book():
    if not request.data or not request.get_json():
        return bad_request('Book details are missing.')
    elif not 'title' in request.get_json() or not request.get_json().get('title'):
        return bad_request('Book title is missing.')
    elif not 'author' in request.get_json() or not request.get_json().get('author'):
        return bad_request('Book author is missing.')
    elif not 'read' in request.get_json():
        return bad_request('Book read is missing.')

    payload = request.get_json()
    BOOKS.append({
        'id': uuid.uuid4().hex,
        'title': payload.get('title'),
        'author': payload.get('author'),
        'read': payload.get('read')
    })
    response = {
        'status': 'success',
        'message': 'Book added.'
    }
    return jsonify(response)

@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    # print(request.data, file=sys.stderr)
    if not request.data or not request.get_json():
        return bad_request('Book details are missing.')
    elif not 'title' in request.get_json() or not request.get_json().get('title'):
        return bad_request('Book title is missing.')
    elif not 'author' in request.get_json() or not request.get_json().get('author'):
        return bad_request('Book author is missing.')
    elif not 'read' in request.get_json():
        return bad_request('Book read is missing.')

    payload = request.get_json()
    for book in BOOKS:
        if book['id'] == book_id:
            book['title'] = payload.get('title')
            book['author'] = payload.get('author')
            book['read'] = payload.get('read')
            response = {
                'status': 'success',
                'message': 'Book updated.'
            }
            return jsonify(response), 200
    return not_found('Book not found.')

@app.route('/books/<string:book_id>', methods=['DELETE'])
def remove_book(book_id):
    global BOOKS
    BOOKS = [book for book in BOOKS if book['id'] != book_id]
    response = {
        'status': 'success',
        'message': 'Book removed.'
    }
    return jsonify(response)

@app.errorhandler(404)
def not_found(message=None):
    message = {
        'status': 'fail',
        'message': message
    }
    response = jsonify(message)
    return response, 404

@app.errorhandler(400)
def bad_request(message=None):
    message = {
        'status': 'fail',
        'message': message
    }
    response = jsonify(message)
    return response, 400


if __name__ == '__main__':
    app.run()
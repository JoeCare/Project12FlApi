"""exc. 12. Booklist REST APIby Sanjay Rai on Pluralsight"""
from flask import Flask, json, request, Response, wrappers
from settings import *
from models import *
from functools import wraps
import datetime
import jwt  # pyjwt packade
# from requests import get, post, delete


# -> time to integrate app.py API with Book model: 7.10 part of Pluralsight course
# -> adding authentication tokens, part: 8.0


def response200(Msg={"Success": "Request fulfilled"}):
    """OK response - request succesfully fulfilled"""
    response = Response(json.dumps(Msg), status=200,
                        mimetype='application/json')
    return response


def response201(reqdata, Msg={"Success": "Object created"}):
    """Succesfully created what was requested for and placed inside specified header"""
    response = Response(json.dumps(Msg),
                        status=201, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(reqdata["isbn"])
    return response


def response204():
    """Request fulfilled - no additional comment"""
    response = Response("", status=204)
    return response


def response400(Msg={"Error": "Invalid input"}):
    """Bad request error - possibly invalid format of provided data"""
    response = Response(json.dumps(Msg),
                        status=400, mimetype='application/json')
    return response


def response404(Msg={"Error": "Requested object not found"}):
    response = Response(json.dumps(Msg), status=404,
                        mimetype='application/json')
    return response


postedCorrectlyMsg = {"postingSuccess": "New BookObject added to storage"}
multipliedObjectMsg = {"duplicationError": "Similar object already stored"}
# multipliedIsbnMsg = {"errorMsg2": "ISBN signature has to be uniqie"}
# books = Book.get_all()

DEFAULT_PAGE_LIMIT = 3

app.config['SECRET_KEY'] = 'gfhg!@Fh56%$&764(*_371(*_&295'


@app.route('/login')
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response("", status=401, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return json.jsonify({'authError': 'Need valid token to proceed'}), 401
    return wrapper


# GET all /books?token=
@app.route('/books')
def get_books():
    return json.jsonify({"books": Book.get_all()})


# GET specific /books/title
@app.route('/books/title=<name>')
def get_book_by_title(name):
    return_value = {}
    for book in Book.get_all():
        if book["name"] == name:
            return_value = {
                "name": book["name"],
                "price": book["price"],
                "isbn": book["isbn"]
            }
    return json.jsonify(return_value)


# GET specific /books/ISBN_NUMBER
@app.route('/books/isbn=<isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_by(isbn)
    return json.jsonify(return_value)


# pre-POST data sanitization
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject
            and len(bookObject) == len(Book.get_all()[0])):
        # I think its more optimized way than in course - hardcoded list of
        # books-dicts will indicate character (length) of json bookObjects
        return True
    else:
        return False


# POST /books as dicts/json
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        if request_data in Book.get_all():
            return response400(multipliedObjectMsg)
        elif Book.add_new(request_data['name'], request_data['price'], request_data['isbn']) == False:
            return response400(multipliedObjectMsg)
        else:
            Book.add_new(request_data['name'],
                         request_data['price'], request_data['isbn'])
            # return response200(postedCorrectlyMsg)
            return response201(request_data, postedCorrectlyMsg)
    else:
        invalidObjectMsg = {
            "ERROR_MSG": "Object passed in request is not valid BookObject.",
            "HELP_MSG": "Use correct syntax example below:",
            "isbn": "0000000000013",
            "name": "title example",
            "price": 9.99
        }
        return response400(invalidObjectMsg)
        #  # json.dumps() dumps pyDictionary to json format;
        #  # it is oposite to json.loads() which translates json to more python-friendly data;
        #  # json.load() translates from file in given filepath;
        # return "False - invalid input"
        # return json.jsonify(request.get_json())  # jsonify() is even more
        #  # user-friendly - makes clean json file from data like this:
        #  # jsonify(id=g.user.id, username=g.user.username, email=g.user.email)
        #  # returns response: {"id": 23, "username": "Jim", "email": "jim@bo.com"}
        #  # arranging Response(dumps(pyDictToJson), and mimetype='application/json')


# @app.route('/booklist', methods=['POST'])
# def add_books():
#     request_data = request.get_json()
#     for data in request_data:
#         print(data)
#         Book.add_new(data['name'], data['price'], data['isbn'])
#     response = Response("", status=204)
#     return response

# PUT needs us to provide whole dataset for particular object which may be inconvinient
def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data and "isbn" in request_data):
        return True
    else:
        return False


def valid_patch_request_data(request_data):
    if("name" in request_data or "price" in request_data):
        return True
    else:
        return False


# PUT /books/1313131313131
# {
#   'name':'Junk',
#   'price':55.66
# }
# PATCH method lets ust update even one specific line (check below)
@app.route('/books/isbn=<isbn>', methods=['PUT'])
@token_required
def replace_book_by(isbn):
    request_data = request.get_json()
    if (not valid_put_request_data(request_data)):
        invalidObjectMsg = {
            "ERROR_MSG": "Object passed in request is not valid BookObject.",
            "HELP_MSG": "Use correct syntax example below:",
            "name": "title example",
            "price": 9.99,
            "isbn": "0000000000013"
        }
        return response400(invalidObjectMsg)
    Book.replace_by(isbn, name=request_data['name'],
                    price=request_data['price'], isbn=request_data['isbn'])
    response = Response("", status=204)
    return response


# PATCH /books/9223177313435
# {
#   'name':'Curious case of the dog night-time',
# }
# PATCH /books/9223177313435
# {
#   'price': 99.99
# }
@app.route('/books/isbn=<isbn>', methods=['PATCH'])
@token_required
def update_by(isbn):
    request_data = request.get_json()
    if (not valid_patch_request_data(request_data)):
        invalidObjectMsg = {
            "ERROR_MSG": "Object passed in request is not valid BookObject.",
            "HELP_MSG": "Correct syntax must cointain at least one of:",
            "name": "title example",
            "price": 9.99
        }
        return response400(invalidObjectMsg)
    if ("name" in request_data):
        Book.replace_by(isbn, name=request_data['name'])
        response = Response("", status=204)
    if ("price" in request_data):
        Book.replace_by(isbn, price=request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# My personal trial - for true DELETE method check funct below
@app.route('/books/<data_string>', methods=['POST'])
def remove_book_by(data_string):
    for book in Book.get_all():
        if data_string in book.values():
            print(book.values())
            try:
                Book.delete_by(data_string)
            except ValueError:
                print(f'Looking for "{data_string}" signature in the storage')
            else:
                response = Response(
                    f'Book with "{data_string}" signature removed from the storage', status=200)
                return response
    response = Response(
        f'Book with "{data_string}" signature not found in the storage', status=404)
    return response


# DELETE books/isbn=<isbn> 6092091445649
@app.route('/books/isbn=<isbn>', methods=['DELETE'])
@token_required
def delete_book_by(isbn):
    if Book.delete_by(isbn):
            # response = Response(
            #     f'Object with {isbn} signature deleted', status=200)
        return response200()
    else:
        invalidObjectMsg = {
            "errorMsg": "Object with ISBN signature provided not found in the storage"
        }
        response = Response(json.dumps(invalidObjectMsg),
                            status=404, mimetype='application/json')
        return response


@app.route('/books/isbns=<int_list:isbns>', methods=['DELETE'])
@token_required
def delete_many(isbns):
    for n in isbns:
        Book.delete_by(n)
    response = Response("", status=204)
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)

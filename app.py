"""
exc. 12. Booklist REST API
by Sanjay Rai on Pluralsight
"""
# from random import randint
# from random import shuffle
from flask import Flask, json, render_template_string, request, Response
from settings import *
from models import *
# -> time to integrate app.py API with Book model: 7.10 part of Pluralsight course


# def ran(x, y):
#     y = y / 2
#     while y > 0:
#         isb = []
#         for n in range(x):
#             n = randint(0, 9)
#             isb.append(str(n))
#         isbn = "".join(isb)
#         print(isbn)
#         shuffle(isb)
#         isbn = "".join(isb)
#         print(isbn)
#         y -= 1

# ran(13, 2)

# nbsi = [n for n in range(13)]
# print(nbsi)

books = [
    {
        "isbn": "8159976278818",
        "name": "Les Miserables",
        "price": 40.99
    },
    {
        "isbn": "1994358200672",
        "name": "Jabberwocky",
        "price": 10
    },
    {
        "isbn": "1090986287649",
        "name": "Dr. Frankenstein",
        "price": 17.99
    },
    {
        "isbn": "6092091445649",
        "name": "War and peace",
        "price": 54.99
    },
    {
        "isbn": "3246466937105",
        "name": "Harry Potter and Chamber of Secrets",
        "price": 61.99
    },
    {
        "isbn": "1099137487649",
        "name": "Anna Karenina",
        "price": 37.99
    },
]


def response200(Msg):
    """OK response - request succesfully fulfilled"""
    response = Response(json.dumps(Msg), status=200,
                        mimetype='application/json')
    return response


def response201(reqdata, Msg):
    """Succesfully created what was requested for and placed inside specified header"""
    response = Response(json.dumps(Msg),
                        status=201, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(reqdata["isbn"])
    return response
    # return response  #  # here we does not saw "True" in body section of Postman at adding new position - client don't have access to resource he create through response body itself, but from particular 'location header'; in Flask we use headers like key:value pairs:


def response400(Msg):
    """Bad request error - invalid format or so"""
    response = Response(json.dumps(Msg),
                        status=400, mimetype='application/json')
    return response


multipliedObjectMsg = {"errorMsg": "Identical object already stored"}


# GET all /books
@app.route('/books')
def get_books():
    return json.jsonify({"books": books})


# GET specific /books/title
@app.route('/books/title=<name>')
def get_book_by_title(name):
    return_value = {}
    for book in books:
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
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                "isbn": book["isbn"],
                "name": book["name"],
                "price": book["price"]
            }
    return json.jsonify(return_value)
    #
    # return render_template_string('<div><h1>Book: {{return_value["name"]}}</h1><p>Found for signature: {{isbn}}</p><p>It costs: {{return_value["price"]}}</p></div>')
    # even more redundant html response
    #
    # return f'Book: {return_value["name"]} \nCost: {return_value["price"]} \nFound for signature: {isbn}'
    # redundant tiral to get text/plain response in API based on json's; d


# pre-POST data sanitization
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject
            and len(bookObject) == len(books[0])):
        # I think its more optimized way than in course - hardcoded list of books-dicts will
        # indicate character (length) of json bookObjects
        return True
    else:
        return False


# POST /books as dicts/json
# { "name":"N", "price": 1.0, "isbn": "1111111111111" }
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        # print(request_data)
        if books.count(request_data) > 0:
            return response400(multipliedObjectMsg)

        elif books.count(request_data) == 0:
            name_int = 1
            for book in books:
                if book["isbn"] == request_data["isbn"]:
                    multipliedIsbnMsg = {
                        "errorMsg2": "ISBN signature has to be uniqie"}
                    return response400(multipliedIsbnMsg)

                elif (book["isbn"] != request_data["isbn"] and book["name"] == request_data["name"]):
                    request_data["name"] = f'{request_data["name"]}-({str(name_int)})'
                    name_int += 1
                    books.insert(0, request_data)
                    postedCorrectlyMsg = {
                        "postedMsg1": "Another instance of BookObject added to storage"}
                    return response201(request_data, postedCorrectlyMsg)

                elif (book["isbn"] != request_data["isbn"] and book["name"] not in request_data["name"]):
                    books.insert(0, request_data)
                    postedCorrectlyMsg = {
                        "postedMsg2": "New BookObject added to storage"}
                    return response201(request_data, postedCorrectlyMsg)

                else:
                    return response400(multipliedObjectMsg)
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


# PUT needs us to provide whole dataset for particular object which may be inconvinient
def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
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
def replace_book_by(isbn):
    request_data = request.get_json()
    if (not valid_put_request_data(request_data)):
        invalidObjectMsg = {
            "ERROR_MSG": "Object passed in request is not valid BookObject.",
            "HELP_MSG": "Use correct syntax example below:",
            "name": "title example",
            "price": 9.99
        }
        return response400(invalidObjectMsg)
    # new_book = json.dumps(request_data)
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = request_data
        i += 1
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
def update_by(isbn):
    request_data = request.get_json()
    updated_book = {}
    if ("name" in request_data):
        updated_book["name"] = request_data["name"]
    if ("price" in request_data):
        updated_book["price"] = request_data["price"]
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# My personal trial - for true DELETE method check funct below
@app.route('/books/<data_string>', methods=['POST'])
def remove_book_by(data_string):
    for book in books:
        if data_string in book.values():
            print(book.values())
            try:
                books.remove(book)
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
def delete_by(isbn):
    # request_data = request.get_json()
    # i = 0
    for n, book in enumerate(books):
        # also better way imho than using additional variable for incrementation
        if book['isbn'] == isbn:
            books.pop(n)
            response = Response(
                f'Object with {isbn} signature deleted', status=200)
            return response
        # i += 1
    invalidObjectMsg = {
        "errorMsg": "Object with ISBN signature provided not found in the storage"
    }
    response = Response(json.dumps(invalidObjectMsg),
                        status=404, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(port=8000, debug=True)

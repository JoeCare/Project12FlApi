from app import app


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


valid_object = {
    'name': 'N',
    'price': 11.99,
    'isbn': "1111111111111"
}

missing_name = {
    'price': 11.99,
    'isbn': "1111111111111"
}

missing_price = {
    'name': 'N',
    'isbn': "1111111111111"
}

missing_isbn = {
    'name': 'N',
    'price': 11.99
}

empty_dictionary = {}

bookz = [valid_object, missing_name,
         missing_price, missing_isbn, empty_dictionary]


# def validateObjects(objects_list):
#     for object in objects_list:
#         print(object)
#         try:
#             if not validBookObject(object):
#                 objects_list.pop(objects_list.index(object))
#         except ValueError:
#             print(
#                 f"Object {objects_list.index(object)}: {object} is invalid. BookObject has to have name, price and isbn.")
#     return objects_list

# def validateObjects(objects_list):
#     books = []
#     invalid = 0
#     for object in objects_list:
#         print(object)
#         if validBookObject(object):
#             books.extend(object.items())
#         else:
#             invalid += 1
#             print("Object invalid. BookObject has to have name, price and isbn.")
#     for book in books:
#         book1 = dict(book[0]=book[1])
#         print(book1)
#         books.extend(book1)
#         print(books)
#     try:
#         if invalid > 0:
#             raise ValueError(
#                 f"Valid BookObject has to have name, price and isbn. Stopped {invalid} invalid objects from posting.")
#             return books
#     except ValueError:
#         print(
#             f"BookObject has to have name, price and isbn. Stopped {invalid} invalid objects from posting.")
#     finally:
#         return books
@app.route('/books/isbn=<isbn>', methods=['PUT'])
def replace_book_by(isbn):
    request_data = request.get_json()
    print(request_data)
    return json.jsonify(request.get_json())

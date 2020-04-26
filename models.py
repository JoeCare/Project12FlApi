from flask import Flask, json
from settings import app
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.engine.default import  # trial of search for sqlite3.IntegrityError: UNIQUE constraint failed: books.isbn
from random import shuffle
from werkzeug.routing import BaseConverter

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.String(13), nullable=False, unique=True)

    def json(self):
        return {"name": self.name, "price": self.price, "isbn": self.isbn}

    # def get_isbn(_istr):
    #     _istr = [_ for _ in _istr]
    #     shuffle(_istr)
    #     result = "".join(_istr)
    #     return result

    def get_all():
        return [Book.json(book) for book in Book.query.all()]

    def get_by(_isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    def add_new(_name, _price, _isbn):
        """Solution for creating name-isbn-uniqe only BookObjects yet """
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        if (Book.query.filter_by(isbn=_isbn).first() == None
                and Book.query.filter_by(name=_name).first() == None):
            db.session.add(new_book)
            db.session.commit()
        # elif (Book.query.filter_by(isbn=_isbn).first() == None and Book.query.filter_by(name=_name).first()):
        # elif Book.query.filter_by(isbn=_isbn).first() == None:
        #     if Book.query.:
        #     new_book.name += f"-({str(len(Book.query.filter_by(name=_name).all()))})"
            # _isbn = [i for i in _isbn]
            # shuffle(_isbn)
            # new_book.isbn = "".join(_isbn)
            # new_book.price = _price
            # new_book.isbn = f"{int(_isbn)+1}"
            # new_book.isbn = "".join(shuffle(_isbn.split(",")))
            # shuffle(new_book.isbn)
            # db.session.add(new_book)
            # db.session.commit()

        # elif (Book.query.filter_by(name=_name).first() == None and Book.query.filter_by(isbn=_isbn).first()):
            # new_book.name = f"{_name}-({str(len(Book.query.filter_by(name=_name).all()))})"
            # new_isbn = Book.get_isbn(_isbn)
            # new_book.isbn = new_isbn
            # _isbn = [i for i in _isbn]
            # shuffle(_isbn)
            # new_book.isbn = "".join(_isbn)
            # new_book.price = _price
            # new_book.isbn = f"{int(_isbn)+1}"
            # new_book.isbn = "".join(shuffle(_isbn.split(",")))
            # shuffle(new_book.isbn)
            # db.session.add(new_book)
            # db.session.commit()
        else:
            return False

    # def add_many(iterable):
    #     new_books = iterable
    #     for book in new_books:

    def delete_by(_isbn):
        # Book.query.filter_by(isbn=_isbn).delete()
        succesfully = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(succesfully)

    def replace_by(_isbn, **kwargs):
        replaced_object = Book.query.filter_by(isbn=_isbn).first()
        if "price" in kwargs.keys():
            replaced_object.price = kwargs["price"]
        if "name" in kwargs.keys():
            replaced_object.name = kwargs["name"]
        if "isbn" in kwargs.keys():
            replaced_object.isbn = kwargs["isbn"]
        db.session.commit()

    # def change_by(_isbn, _name, _price):
    #     """Imho redundant with replace_by written as above"""
    #     replaced_object = Book.query.filter_by(isbn=_isbn).first()
    #     print(type(replaced_object))
    #     replaced_object.price = _price
    #     replaced_object.name = _name
    #     db.session.commit()

    def __repr__(self):
        book_object = {
            "name": self.name,
            "price": self.price,
            "isbn": self.isbn
        }
        return json.dumps(book_object)
        # used only for console info


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })

    def username_password_match(_username, _password):
        user = User.query.filter_by(username=_username).filter_by(
            password=_password).first()
        if user is None:
            return False
        else:
            return True

    def get_all():
        return User.query.all()

    def create(_username, _password):
        new_user = User(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()


class IntListUrl(BaseConverter):

    regex = r'\d+(?:;\d+)*;?'

    # this is used to parse the url and pass the list to the view function
    def to_python(self, value):
        return [int(x) for x in value.split(';')]

    # this is used when building a url with url_for
    def to_url(self, value):
        return ';'.join(str(x) for x in value)


app.url_map.converters['int_list'] = IntListUrl

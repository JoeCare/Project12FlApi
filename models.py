from flask import Flask, json
from settings import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.String(13), nullable=False, unique=True)

    def json(self):
        return {"name": self.name, "price": self.price, "isbn": self.isbn}

    def add_new(_name, _price, _isbn):
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()

    def get_all():
        return [Book.json(book) for book in Book.query.all()]

    def get_by(_isbn):
        return Book.query.filter_by(isbn=_isbn).first()

    def delete_by(_isbn):
        Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()

    def change_by(_isbn, **kwargs):
        replaced_object = Book.query.filter_by(isbn=_isbn).first()
        if "price" in kwargs.keys():
            replaced_object.price = kwargs["price"]
        if "name" in kwargs.keys():
            replaced_object.name = kwargs["name"]
        db.session.commit()

    def replace_by(_isbn, _name, _price):
        replaced_object = Book.query.filter_by(isbn=_isbn).first()
        print(type(replaced_object))
        replaced_object.price = _price
        replaced_object.name = _name
        db.session.commit()

    def __repr__(self):
        book_object = {
            "name": self.name,
            "price": self.price,
            "isbn": self.isbn
        }
        return json.dumps(book_object)
        # used only for console info

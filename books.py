import json

from flask import Blueprint, request
from models import Books, Loans, db

books = Blueprint('/books', __name__, url_prefix='/books')

def check_availability(book_id):
    loan_of_the_book = Loans.query.filter_by(id=book_id, is_active=True).first()
    if loan_of_the_book: 
        return False
    else:
        return True

@books.route('', methods=['GET', 'POST'])
@books.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def crud_loans(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        book_name = request_data['book_name']
        author = request_data['author']
        published_year = request_data['published_year']
        book_type = request_data['book_type']

        newBook = Books(book_name, author, published_year, book_type)
        db.session.add(newBook)
        db.session.commit()
        return {"message":"a new book  was created"} 

    if request.method == 'GET':
        if id == -1:
            res = []
            for book in Books.query.all():
                loan = Loans.query.filter_by(book_id=book.id, is_active=True).first()
                is_loaned = True if loan else False
                res.append(
                    {
                        "id": book.id,
                        "book_name": book.book_name, 
                        "author": book.author, 
                        "published_year": book.published_year,
                        "book_type": book.book_type,
                        "is_active": book.is_active,
                        "is_loaned": is_loaned,
                        "loan_id": loan.id if loan else "",
                        "return_date": str(loan.return_date) if loan else ""
                        }
                    )
            return (json.dumps(res))      
        else: 
            res = []
            book = Books.query.filter_by(id=id).first()
            res.append(
                    {"id": book.id, "book_name": book.book_name, "author": book.author, "published_year": book.published_year,"book_type": book.book_type, "is_active": book.is_active})
            return (json.dumps(res))

    if request.method == 'DELETE': 
        del_book = Books.query.filter_by(id=id, is_active=True).first()
        if del_book is None:
            return {"message": "book not found."}
        if not check_availability(id):
            return {"mesage": "can't delete the book because the book is on loan"}
        else:
            del_book.is_active = False
            db.session.commit()
            return {"message":"book was deleted" } 

    if request.method == 'PUT': 
        request_data = request.get_json()
        upd_book= Books.query.filter_by(id=id).first()
        upd_book.book_name = request_data['book_name']
        upd_book.author = request_data['author']
        upd_book.book_type = request_data['book_type']
        upd_book.is_active = bool(request_data['is_active'])
        db.session.commit()
        return {"message":"a book was updated"}


import json
from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_cors import CORS
from models import Books, Customers, Loans, db

loans = Blueprint('/loans', __name__, url_prefix='/loans')

def get_delta(borrow_type):
    if borrow_type == 1:
        delta = 10
    elif borrow_type == 2:
        delta = 5
    else:
        delta = 2
    return delta

def check_availability(book_id):
    loan_of_the_book = Loans.query.filter_by(book_id=book_id, is_active=True).first()
    if loan_of_the_book: 
        return False
    else:
        return True

@loans.route('', methods=['GET', 'POST'])
@loans.route('/<id>', methods=['GET', 'DELETE', 'PUT'])
def crud_loans(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        customer_id = request_data['customer_id']
        book_id = request_data['book_id']
        book = Books.query.filter_by(id=book_id, is_active=True).first()
        if book is None:
            return {"mesage": "can't loan the book because book doesn't exist"}
        customer = Customers.query.filter_by(id=customer_id, is_active=True).first()
          # fetching customer from db
        if customer is None:
            return {"mesage": "can't loan the book because customer doesn't exist"}
        if customer.amount_to_loan == 0:
            return {"mesage": "can't loan the book because customer loaned the max amount of books"}
        if not check_availability(book_id):
            return {"mesage": "can't loan the book because the book was already loaned"}

        loan_date = datetime.now()
        book_to_borrow = Books.query.filter_by(id=book_id).first()
        borrow_type = book_to_borrow.book_type
        delta = get_delta(borrow_type)
        return_date = loan_date + timedelta(days=delta)
    
        newLoan = Loans(customer_id, book_id, loan_date, return_date ) ## create new Loand object in RAM
        db.session.add(newLoan)
        db.session.commit()
         # creates sql query and creates in db
        customer.amount_to_loan = customer.amount_to_loan - 1
        db.session.commit()
        
        return {"message": "a new loan  was created"}

    if request.method == 'GET':
        if id == -1:
            res = []
            for loan in Loans.query.filter_by(is_active=True):
                customer = Customers.query.filter_by(id=loan.customer_id, is_active=True).first()
                book = Books.query.filter_by(id=loan.book_id, is_active=True).first()
                res.append(
                    {
                        "id": loan.id,
                        "customer_id": loan.customer_id,
                        "book_id": loan.book_id, 
                        "loan_date": str(loan.loan_date), 
                        "return_date": str(loan.return_date), 
                        "is_active": loan.is_active,
                        "customer_name": customer.customer_name,
                        "phone_number": customer.phone_number,
                        "book_name": book.book_name 
                    
                     }
                    )
            return (json.dumps(res))
        else: 
            res = []
            loan = Loans.query.filter_by(id=id).first()
            res.append(
                    {"id": loan.id, "customer_id": loan.customer_id, "book_id": loan.book_id, "loan_date": str(loan.loan_date), "return_date": str(loan.return_date), "is_active": loan.is_active})
            return (json.dumps(res))
            

    if request.method == 'DELETE':
        loan = Loans.query.filter_by(id=id).first()
        loan.is_active = False
        customer = Customers.query.filter_by(id=loan.customer_id, is_active=True).first()
        customer.amount_to_loan = customer.amount_to_loan + 1 # update the customer amount to loan in the db first fetch(customer) and then update
        db.session.commit()
        return {"message": "loan was updated as inactive"}
        

    if request.method == 'PUT':
        request_data = request.get_json()
        upd_loan = Loans.query.filter_by(id=id).first()
        return_date = datetime.strptime(request_data['return_date'] , '%Y-%m-%d').date()
        upd_loan.return_date = return_date
        db.session.commit()
        return {"message": "a loan was updated"}

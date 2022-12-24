from flask_sqlalchemy import SQLAlchemy

MAX_LOAN_PER_CUSTOMER = 3

db = SQLAlchemy()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    published_year = db.Column(db.Integer)
    book_type = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)

    books = db.relationship('Loans', backref='books')

    def __init__(self, book_name, author, published_year, book_type):
        self.book_name = book_name
        self.author = author
        self.published_year = published_year
        self.book_type = book_type
        self.is_active = True


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(11)) 
    amount_to_loan = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)
   
    customers = db.relationship('Loans', backref='customers')

    def __init__(self, customer_name, city, age, phone_number):
        self.customer_name = customer_name
        self.city = city
        self.age = age
        self.phone_number = phone_number
        self.amount_to_loan = MAX_LOAN_PER_CUSTOMER
        self.is_active = True

class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    loan_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean)
   
    def __init__(self, customer_id, book_id, loan_date, return_date):
        self.customer_id = customer_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_active = True

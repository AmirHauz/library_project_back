from books import books
from customers import customers
from flask import Flask
from flask_cors import CORS
from loans import loans
from models import db

print(f"!!!!!!!!!!! {__name__}")
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"


db.init_app(app)
with app.app_context():
    db.create_all()

print ("outside has run")
print(f"{__name__}")

app.register_blueprint(books)
app.register_blueprint(customers)
app.register_blueprint(loans)

@app.route("/")
def home():
    return "i am the app page!! and i am here"


if __name__ == '__main__':
    print ("main init has run")    
    app.run(debug=True)

# Library Project 
The project was to built a system for librarian. Front and Back.

## Back:
In back I created 5 modules:
### app.py:
    Creating blueprints and mapping between the other modules.
### models.py:
    Creating database and its tables.
### books.py
    CRUD for books
### customers.py
    CRUD for customers
## loans.py
    CRUD for loans

## front:
    In front 6 pages that in them i made the crud to work.
    The navbar is connecting to page that do the action written on the navbar.
### index.html
    the links that lead to it in the navbar are:picture, Home, Loans->Loan, Loans->Return, Books-> delete
    it is getting list of book that are active. can be searched by the name of the book and by the name of the author. 
#### bottons:
    -Return - active just if the book is loaned- by pressing it, the loan is returned.(the delete in the crud of loans)
    -Loan- active just if the book is available(returned).
    opening modal that contain the name of book and the author that the customer want to loan . 
    and all the customers that can loan.
     It have a search box to narrow them down by name.
     the botton Create Loan in the modal is creating a new loan (the post in the crud of loans) 
    -Delete - active just if the book is not loaned. It is deleting book(the delete in the crud of books).
    comment: it is not really deleting it. it is deactivate it. in order to make it appear again in the book list,
     the only option to activate again is by books_update.html(the idea is if a customer lost a book in the past and found it for example.)
### books_new.html
    the link that lead to it in the navbar is: Books -> New.
    It is leading to a form with fields that are needed in order to create a new book.(the post in the crud of books)
### book_update.html
    the link that lead to it in the navbar is: Books -> Update.
    it is getting list of book that can be searched by the name of the book and by the name of the author. 
#### bottons:
    -Update-
    opening modal that contains the information that is already in the book. 
    the librarian decide what to change and press update (the put in the crud of books)    
### customers_exist.html
    the link that lead to it in the navbar is: customer -> Existing.
     it is getting list of customers that can be searched by the name of the customer and by  phone number. 
#### bottons:
    -Delete- is activated just if the customer is_active. the only way to activate it again is by using update.(the delete in the crud of customers)
    -Update-
    opening modal that contains the information that is already in the customer. 
    the librarian decide what to change and press update (the put in the crud of customers)   
### customers_new.html
    the link that lead to it in the navbar is: Customers -> New.
    It is leading to a form with fields that are needed in order to create a new customer.(the post in the crud of customer)
### loan_extend.html
     the link that lead to it in the navbar is: Loans -> Extend.
     it is getting list of active loans that can be searched by the name of the customer, phone number or by name of book. 
#### bottons:
    -Extend-
    opening modal that contains the information of the customer and the information of the book. 
    it have a table of dates to pick.
    and a Submit button that is updating the loan date (the put in the crud of loans)

## comments:
    in my view of thing nothing can be deleted in the library this is why all the "delete" mathod
     are updating to not active. and they are still saved in database.
import json

from flask import Blueprint, request
from models import MAX_LOAN_PER_CUSTOMER, Customers, db

customers = Blueprint('/customers', __name__, url_prefix='/customers')

@customers.route('', methods=['GET', 'POST'])
@customers.route('/<id>', methods=['GET', 'DELETE', 'PUT'])
def crud_customers(id=-1):
    
    if request.method == 'POST':
        request_data = request.get_json()
        customer_name = request_data['customer_name']
        city = request_data['city']
        age = request_data['age']
        phone_number = request_data['phone_number']
        newCostumer = Customers(customer_name, city, age, phone_number)
        db.session.add(newCostumer)
        db.session.commit()
        return {"message": "a new customer  was created"}

    if request.method == 'GET':
        if id ==-1:
            res = []
            for customer in Customers.query.all(): # todo: check if all can be removed
                res.append(
                {"id": customer.id, "customer_name": customer.customer_name, "city": customer.city, "age": customer.age,
                "phone_number": customer.phone_number,"amount_to_loan": customer.amount_to_loan, "is_active": customer.is_active})
            return (json.dumps(res))
        else:
            res = []
            customer = Customers.query.filter_by(id=id).first()
            res.append(
                {"id": customer.id, "customer_name": customer.customer_name, "city": customer.city, "age": customer.age,
                "phone_number": customer.phone_number,"amount_to_loan": customer.amount_to_loan, "is_active": customer.is_active})
            return (json.dumps(res))

    if request.method == 'DELETE':
        del_customer = Customers.query.filter_by(id=id, is_active=True).first()
        if del_customer is None:
            return {"message": "Customer not found."}
        if del_customer.amount_to_loan < MAX_LOAN_PER_CUSTOMER:
            return {"message": f"Cannot delete a customer while they have books loaned. Books loaned = {MAX_LOAN_PER_CUSTOMER - del_customer.amount_to_loan}"}
        del_customer.is_active = False
        db.session.commit()
        return {"message": "customer was deactivated"}

    if request.method == 'PUT':
        request_data = request.get_json()
        upd_customer = Customers.query.filter_by(id=id).first()
        upd_customer.customer_name = request_data['customer_name']
        upd_customer.city = request_data['city']
        upd_customer.age = request_data['age']
        upd_customer.phone_number = request_data['phone_number']
        upd_customer.is_active = bool(request_data['is_active'])
        
        db.session.commit()
        return {"message": "a customer was updated"}

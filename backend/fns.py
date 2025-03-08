from models import db, User, Customer, Professional, Service, ServiceRequest
from flask import session
from sqlalchemy import select, delete, update
from sqlalchemy.sql import or_, and_
from bcrypt import gensalt, hashpw, checkpw


# AUTHENTICATION
def login(user_obj):
    session["user"] = user_obj.email
    return { "msg": "LOGGED IN", "user": user_obj.email, "role": user_obj.role }


def logout(user_obj):
    session.pop("user", None)
    return { "msg": "LOGGED OUT" }


def check_session():
    if "user" in session:
        return { "logged_in": True, "user": session["user"] }
    else:
        return { "logged_in": False }


# PASSWORDS
def gen_hash(passwd):
    salt = gensalt()
    hashed = hashpw(passwd.encode(), salt)
    return hashed.decode()


def check_pw(entered, hashed):
    return checkpw(entered.encode(), hashed.encode())


# GETTING MULTIPLES
def get_all(model, ids=None):
    if ids:
        sql = select(model).where(model.id.in_(ids)).order_by(model.id)
    else:
        sql = select(model).order_by(model.id)
    results = db.session.scalars(sql)
    return results


def get_all_customers(ids=None):
    return get_all(Customer, ids=ids)


def get_all_professionals(ids=None):
    return get_all(Professional, ids=ids)


def get_all_services(ids=None):
    return get_all(Service, ids=ids)


def get_all_requests(ids=None):
    return get_all(ServiceRequest, ids=ids)


def search_professional_objects(parameter, query):
    if (query == ""):
        return get_all_professionals()
    
    query = '%' + query + '%'
    if parameter == "professional_name":
        sql = select(Professional).join(User).where(User.fullname.ilike(query))
    elif parameter == "professional_email":
        sql = select(Professional).join(User).where(User.email.ilike(query))
    elif parameter == "professional_contact":
        sql = select(Professional).where(Professional.contact.ilike(query))
    elif parameter == "professional_address":
        sql = select(Professional).where(Professional.address.ilike(query))
    elif parameter == "professional_pincode":
        sql = select(Professional).where(Professional.pincode.ilike(query))
    return db.session.scalars(sql)


def search_customer_objects(parameter, query):
    if (query == ""):
        return get_all_customers()

    query = '%' + query + '%'
    if parameter == "customer_name":
        sql = select(Customer).join(User).where(User.fullname.ilike(query))
    elif parameter == "customer_email":
        sql = select(Customer).join(User).where(User.email.ilike(query))
    elif parameter == "customer_contact":
        sql = select(Customer).where(Customer.contact.ilike(query))
    elif parameter == "customer_address":
        sql = select(Customer).where(Customer.address.ilike(query))
    elif parameter == "customer_pincode":
        sql = select(Customer).where(Customer.pincode.ilike(query))
    return db.session.scalars(sql)


def search_service_objects(parameter, query):
    if (query == ""):
        return get_all_services()

    if parameter == "service_name":
        query = '%' + query + '%'
        sql = select(Service).where(Service.name.ilike(query))
    elif parameter == "service_description":
        query = '%' + query + '%'
        sql = select(Service).where(Service.description.ilike(query))
    elif parameter == "service_price":
        sql = select(Service).where(Service.price == query)
    return db.session.scalars(sql)


def search_request_objects(parameter, query):
    if (query == ""):
        return get_all_requests()

    query = '%' + query + '%'
    if parameter == "request_service_name":
        sql = select(ServiceRequest).join(Service).where(Service.name.ilike(query))
    elif parameter == "request_customer_name":
        sql = select(ServiceRequest).join(Customer).join(User, Customer.user_id == User.id).where(User.fullname.ilike(query))
    elif parameter == "request_professional_name":
        sql = select(ServiceRequest).join(Professional, ServiceRequest.professional_id == Professional.id).join(User, Professional.user_id == User.id).where(User.fullname.ilike(query))
    return db.session.scalars(sql)


def search_objects(parameter, query):
    if parameter.startswith("professional"):
        return search_professional_objects(parameter, query)
    elif parameter.startswith("customer"):
        return search_customer_objects(parameter, query)
    elif parameter.startswith("service"):
        return search_service_objects(parameter, query)
    elif parameter.startswith("request"):
        return search_request_objects(parameter, query)


def delete_all_with_ids(model, ids):
    sql = delete(model).where(model.id.in_(ids))
    db.session.execute(sql)
    db.session.commit()


def delete_services_with_ids(ids):
    delete_all_with_ids(Service, ids)


def delete_requests_with_ids(ids):
    delete_all_with_ids(ServiceRequest, ids)


def update_professional_status(ids, approval):
    profs = get_all_professionals(ids=ids)
    for prof in profs:
        prof.approval = approval
    db.session.commit()

def update_customer_status(ids, status):
    customers = get_all_customers(ids=ids)
    for customer in customers:
        customer.status = status
    db.session.commit()


# GETTING SINGLES
def get_with_id(model, pkid):
    sql = select(model).where(model.id == pkid)
    result = db.session.scalars(sql).first()
    return result

def get_professional_with_id(id):
    return get_with_id(Professional, id)

def get_customer_with_id(id):
    return get_with_id(Customer, id)

def get_service_with_id(id):
    return get_with_id(Service, id)

def get_request_with_id(id):
    return get_with_id(ServiceRequest, id)

def get_user_with_id(id):
    return get_with_id(User, id)

def get_user_with_creds(email, passwd):
    sql = select(User).filter(User.email == email)
    user = db.session.scalars(sql).first()
    if user and check_pw(passwd, user.password):
        return user
    return None

def update_service_with_id(id, editdata):
    service = get_service_with_id(id)
    service.name = editdata.get("name")
    service.description = editdata.get("description")
    service.price = editdata.get("price")
    service.timereq = editdata.get("timereq")
    db.session.commit()

def delete_with_id(model, pkid):
    sql = delete(model).where(model.id == pkid)
    db.session.execute(sql)
    db.session.commit()

def delete_service_with_id(id):
    delete_with_id(Service, id)

# MANAGEMENT

def add_customer_user(user_data, cust_data):
    user = User(**user_data)
    customer = Customer(**cust_data)
    customer.user = user
    db.session.add(customer)
    db.session.commit()


def add_service(service_data):
    service = Service(**service_data)
    if service.service_exists():
        return { "added": False, "message": "Service Already Exists" }
    db.session.add(service)
    db.session.commit()
    return { "added": True, "message": "Service Added Successfully" }



def add_professional_user(user_data, prof_data):
    user = User(**user_data)
    professional = Professional(**prof_data)
    professional.user = user
    db.session.add(professional)
    db.session.commit()



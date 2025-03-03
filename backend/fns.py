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


# MODELS

# GETTING MULTIPLES
def get_all(model, ids=None):
    if ids:
        sql = select(model).where(model.id.in_(ids)).order_by(model.id)
    else:
        sql = select(model).order_by(model.id)
    results = db.session.scalars(sql)
    return results

def get_all_customers():
    return get_all(Customer)

def get_all_professionals():
    return get_all(Professional)

def get_all_services():
    return get_all(Service)

def get_all_requests():
    return get_all(ServiceRequest)

def delete_all_with_ids(model, ids):
    sql = delete(model).where(model.id.in_(ids))
    db.session.execute(sql)
    db.session.commit()

def delete_services_with_ids(ids):
    delete_all_with_ids(Service, ids)

def update_professional_status(ids, approval):
    profs = get_all(Professional, ids=ids)
    for prof in profs:
        prof.approval = approval
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
    user = get_with_id(User, id)
    return user

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



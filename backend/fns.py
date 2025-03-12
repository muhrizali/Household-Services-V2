from models import db, User, Customer, Professional, Service, ServiceRequest
from sqlalchemy import select, delete
from sqlalchemy.sql import or_, and_
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from flask_jwt_extended import create_access_token
from redis import Redis
import json


# CACHING FROM DB
redis_client = Redis(decode_responses=True)

def cache_users():
    users = get_all(User)
    user_dict_list = [user.to_dict() for user in users]
    redis_client.setex("USER_ALL", 60, json.dumps(user_dict_list))

def cache_customers():
    customers = get_all(Customer)
    customer_dict_list = [customer.to_dict() for customer in customers]
    redis_client.setex("CUSTOMER_ALL", 60, json.dumps(customer_dict_list))

def cache_professionals():
    professionals = get_all(Professional)
    professional_dict_list = [professional.to_dict() for professional in professionals]
    redis_client.setex("PROFESSIONAL_ALL", 60, json.dumps(professional_dict_list))

def cache_services():
    services = get_all(Service)
    service_dict_list = [service.to_dict() for service in services]
    redis_client.setex("SERVICE_ALL", 60, json.dumps(service_dict_list))

def cache_service_requests():
    service_requests = get_all(ServiceRequest)
    service_request_dict_list = [service_request.to_dict() for service_request in service_requests]
    redis_client.setex("SERVICE_REQUEST_ALL", 60, json.dumps(service_request_dict_list))

def cache_db():
    cache_users()
    cache_customers()
    cache_professionals()
    cache_services()
    cache_service_requests()


# AUTHENTICATION
def login_user(user_obj):
    access_token = create_access_token(user_obj.username)
    if user_obj.role == "CUSTOMER":
        return {
            "access_token": access_token,
            "logged_in": True,
            "id": user_obj.get_customer().id,
            "user": user_obj.email, 
            "role": "CUSTOMER", 
        }
    elif user_obj.role == "PROFESSIONAL":
        return {
            "access_token": access_token,
            "logged_in": True,
            "id": user_obj.get_prof().id,
            "user": user_obj.email, 
            "role": "PROFESSIONAL", 
        }
    elif user_obj.role == "ADMIN":
        return {
            "access_token": access_token,
            "logged_in": True,
            "user": user_obj.email, 
            "role": "ADMIN",
        }



def logout():
    # session.pop("user", None)
    return { "logged_out": True }


# PASSWORDS
def gen_hash(passwd):
    salt = gensalt()
    hashed = hashpw(passwd.encode(), salt)
    return hashed.decode()


def check_pw(entered, hashed):
    return checkpw(entered.encode(), hashed.encode())




# GETTING MULTIPLE DB OBJECTS
def get_all(model, ids=None):
    if ids:
        sql = select(model).where(model.id.in_(ids)).order_by(model.id)
    else:
        sql = select(model).order_by(model.id)
    results = db.session.scalars(sql)
    return results


def get_all_customers(ids=None):
    if redis_client.exists("CUSTOMER_ALL"):
        customer_all_dict_list = json.loads(redis_client.get("CUSTOMER_ALL"))
        return customer_all_dict_list

    customer_all = get_all(Customer, ids=ids)
    customer_all_dict_list = [customer.to_dict() for customer in customer_all]
    redis_client.setex("CUSTOMER_ALL", 60, json.dumps(customer_all_dict_list))
    return customer_all_dict_list


def get_all_professionals(ids=None):
    if redis_client.exists("PROFESSIONAL_ALL"):
        professional_all_dict_list = json.loads(redis_client.get("PROFESSIONAL_ALL"))
        return professional_all_dict_list

    professional_all = get_all(Professional, ids=ids)
    professional_all_dict_list = [professional.to_dict() for professional in professional_all]
    # redis_client.setex("PROFESSIONAL_ALL", 60, json.dumps(professional_all_dict_list))
    return professional_all_dict_list


def get_all_services(ids=None):
    if redis_client.exists("SERVICE_ALL"):
        service_all_dict_list = json.loads(redis_client.get("SERVICE_ALL"))
        return service_all_dict_list

    service_all = get_all(Service, ids=ids)
    service_all_dict_list = [service.to_dict() for service in service_all]
    redis_client.setex("SERVICE_ALL", 60, json.dumps(service_all_dict_list))
    return service_all_dict_list


def get_all_requests(ids=None):
    if redis_client.exists("SERVICE_REQUEST_ALL"):
        service_request_all_dict_list = json.loads(redis_client.get("SERVICE_REQUEST_ALL"))
        return service_request_all_dict_list

    service_request_all = get_all(ServiceRequest, ids=ids)
    service_request_all_dict_list = [service_request.to_dict() for service_request in service_request_all]
    redis_client.setex("SERVICE_REQUEST_ALL", 60, json.dumps(service_request_all_dict_list))
    return service_request_all_dict_list



# GETTING SINGLE DB OBJECTS
def get_with_id(model, pkid):
    sql = select(model).where(model.id == pkid)
    result = db.session.scalars(sql).first()
    return result

def get_professional_with_id(id):
    professional_all_dict_list = get_all_professionals()
    def extract(prof_data):
        return prof_data.get('id') == id
    professional_dict = list(filter(extract, professional_all_dict_list))[0]
    return professional_dict

def get_customer_with_id(id):
    customer_all_dict_list = get_all_customers()
    def extract(customer):
        return customer.get('id') == id
    customer_dict = list(filter(extract, customer_all_dict_list))[0]
    return customer_dict

def get_service_with_id(id):
    service_all_dict_list = get_all_services()
    def extract(service):
        return service.get('id') == id
    service_dict = list(filter(extract, service_all_dict_list))[0]
    return service_dict

def get_request_with_id(id):
    service_request_all_dict_list = get_all_requests()
    def extract(service_request):
        return service_request.get('id') == id
    service_request_dict = list(filter(extract, service_request_all_dict_list))[0]
    return service_request_dict

def get_user_with_id(id):
    return get_with_id(User, id)

def get_user_with_username(username):
    sql = select(User).filter(User.username == username)
    return db.session.scalars(sql).first()

def get_user_with_creds(email, passwd):
    sql = select(User).filter(User.email == email)
    user = db.session.scalars(sql).first()
    if user and check_pw(passwd, user.password):
        return user
    return None



# SEARCHING FUNCTIONS
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


# MANAGEMENT DB FUNCTIONS
def delete_all_with_ids(model, ids):
    sql = delete(model).where(model.id.in_(ids))
    db.session.execute(sql)
    db.session.commit()


def delete_services_with_ids(ids):
    delete_all_with_ids(Service, ids)
    cache_services()


def delete_requests_with_ids(ids):
    delete_all_with_ids(ServiceRequest, ids)
    cache_service_requests()


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


def update_service_with_id(id, editdata):
    service = get_service_with_id(id)
    service.name = editdata.get("name")
    service.description = editdata.get("description")
    service.price = editdata.get("price")
    service.timereq = editdata.get("timereq")
    db.session.commit()


def update_service_request_with_id(id, editdata):
    service_request = get_request_with_id(id)
    service_request.remarks = editdata.get("remarks")
    completed = datetime.strptime(editdata.get("completed"), "%Y-%m-%d %H:%M:%S")
    service_request.completed = completed
    db.session.commit()


def delete_with_id(model, pkid):
    sql = delete(model).where(model.id == pkid)
    db.session.execute(sql)
    db.session.commit()

def delete_service_with_id(id):
    delete_with_id(Service, id)


def add_customer_user(user_data, cust_data):
    user = User(**user_data)
    customer = Customer(**cust_data)
    customer.user = user
    db.session.add(customer)
    db.session.commit()
    cache_users()
    cache_customers()


def add_service(service_data):
    service = Service(**service_data)
    if service.service_exists():
        return { "added": False, "message": "Service Already Exists" }
    db.session.add(service)
    db.session.commit()
    cache_services()
    return { "added": True, "message": "Service Added Successfully" }


def add_professional_user(user_data, prof_data):
    user = User(**user_data)
    professional = Professional(**prof_data)
    professional.user = user
    db.session.add(professional)
    db.session.commit()
    cache_professionals()







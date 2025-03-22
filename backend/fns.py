from models import db, User, Customer, Professional, Service, ServiceRequest
from sqlalchemy import select, delete
from sqlalchemy.sql import or_, and_
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from flask import url_for
from flask_jwt_extended import create_access_token
from redis import Redis
from apps import celery_app as capp
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from os import listdir, remove
from mailcreds import EMAIL_ADDRESS, EMAIL_PASSWORD
from email.message import EmailMessage
import smtplib
import json, csv


# Setting up scheduling for celery
# @capp.on_after_finalize.connect
# def setup_periodic_tasks(sender: Celery, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute=1),
#         generate_csv_report_task.s(),
#         name='generate report every minute'
#     )

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
            "useremail": user_obj.email, 
            "username": user_obj.username, 
            "role": "CUSTOMER", 
        }
    elif user_obj.role == "PROFESSIONAL":
        return {
            "access_token": access_token,
            "logged_in": True,
            "id": user_obj.get_prof().id,
            "useremail": user_obj.email, 
            "username": user_obj.username, 
            "role": "PROFESSIONAL", 
        }
    elif user_obj.role == "ADMIN":
        return {
            "access_token": access_token,
            "logged_in": True,
            "useremail": user_obj.email, 
            "username": user_obj.username, 
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

def get_all_professionals_with_sid(sid):
    professionals = get_all_professionals()
    def extract_professionals(professional):
        return professional['service']['id'] == sid
    filtered = list(filter(extract_professionals, professionals))
    return filtered


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

def get_all_requests_with_cid(cid):
    service_requests = get_all_requests()
    def extract_service_requests(service_request):
        return service_request['customer']['id'] == cid
    filtered = list(filter(extract_service_requests, service_requests))
    return filtered

def get_assigned_requests_with_pid(pid):
    service_requests = get_all_requests()
    def extract_assigned_requests(service_request):
        return (service_request['status'] == 'ASSIGNED' and service_request['professional']['id'] == pid)
        # return (service_request['professional']['id'] == pid)
    filtered = list(filter(extract_assigned_requests, service_requests))
    return filtered

def get_new_requests_with_pid(pid):
    service_requests = get_all_requests()
    def extract_assigned_requests(service_request):
        return (service_request['status'] == 'REQUESTED' and service_request['professional'] and service_request['professional']['id'] == pid)
    filtered = list(filter(extract_assigned_requests, service_requests))
    return filtered

def get_closed_requests_with_pid(pid):
    service_requests = get_all_requests()
    def extract_assigned_requests(service_request):
        return (service_request['status'] == 'CLOSED' and service_request['professional'] and service_request['professional']['id'] == pid)
    filtered = list(filter(extract_assigned_requests, service_requests))
    return filtered



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
        return get_all(Professional)
    
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
        return get_all(Customer)

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
        return get_all(Service)

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
        return get_all(ServiceRequest)
    query = '%' + query + '%'
    if parameter == "request_service_name":
        sql = select(ServiceRequest).join(Service).where(Service.name.ilike(query))
    elif parameter == "request_customer_name":
        sql = select(ServiceRequest).join(Customer).join(User, Customer.user_id == User.id).where(User.fullname.ilike(query))
    elif parameter == "request_professional_name":
        sql = select(ServiceRequest).join(Professional, ServiceRequest.professional_id == Professional.id).join(User, Professional.user_id == User.id).where(User.fullname.ilike(query))
    return db.session.scalars(sql)

def search_request_objects_with_pid(pid, parameter, query):
    if (query == ""):
        sql = select(ServiceRequest).where(ServiceRequest.professional_id == pid)
        return db.session.scalars(sql)
    query = '%' + query + '%'
    if parameter == "request_service_name":
        sql = select(ServiceRequest).join(Service).where(
            and_(
                Service.name.ilike(query),
                ServiceRequest.professional_id == pid
        ))
    elif parameter == "request_customer_name":
        sql = select(ServiceRequest).join(Customer).join(User, Customer.user_id == User.id).where(
            and_(
                User.fullname.ilike(query),
                ServiceRequest.professional_id == pid
            )
    )
    elif parameter == "request_professional_name":
        sql = select(ServiceRequest).join(Professional, ServiceRequest.professional_id == Professional.id).join(User, Professional.user_id == User.id).where(
            and_(
                User.fullname.ilike(query),
                ServiceRequest.professional_id == pid
            )
        )
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


# GENERATING REPORTS FUNCTIONS
@capp.task
def generate_csv_report_task():
    service_requests = get_all(ServiceRequest)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(f'static/reports/REPORT-{timestamp}.csv', mode='w') as csvfile:
        fieldnames = [
            "REQUEST_ID",
            "SERVICE_ID",
            "SERVICE_NAME",
            "CUSTOMER_ID",
            "CUSTOMER_NAME",
            "PROFESSIONAL_ID",
            "PROFESSIONAL_NAME",
            "STATUS",
            "RATING",
            "REMARKS",
            "COMPLETED",
            "CREATED",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # writer.writerow(service_requests[1].to_csv_dict())
        for sr in list(service_requests):
            writer.writerow(sr.to_csv_dict())
def generate_csv_report():
    generate_csv_report_task.delay()


def get_csv_report_urls():
    server_url = 'http://localhost:5000'
    reports_dir = 'static/reports/'
    report_names = listdir(reports_dir)
    urls = []
    for i in range(len(report_names)):
        url = server_url + url_for('static', filename=f'reports/{report_names[i]}')
        ind = i + 1
        urls.append({ 'id': ind, 'url': url, 'name': report_names[i] })
    return urls


def delete_csv_report(name):
    reports_dir = 'static/reports/'
    remove(reports_dir + name)


# SENDING EMAILS
@capp.task
def send_email_to_task(professional_email, customer_name, service_name):
    msg = EmailMessage()
    msg['Subject'] = 'New Service Request for You'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = professional_email
    msg.set_content(f'Customer "{customer_name}" created Service Request "{service_name}" to you. Kindly respond to it as soon as possible.')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
def send_email_to(professional_email, customer_name, service_name):
    send_email_to_task.delay(professional_email, customer_name, service_name)



# MANAGEMENT DB FUNCTIONS
def delete_all_with_ids(model, ids):
    sql = delete(model).where(model.id.in_(ids))
    db.session.execute(sql)
    db.session.commit()


@capp.task
def delete_services_with_ids_task(ids):
    delete_all_with_ids(Service, ids)
    cache_services()
def delete_services_with_ids(ids):
    # CELERY
    delete_services_with_ids_task.delay(ids)


@capp.task
def delete_requests_with_ids_task(ids):
    delete_all_with_ids(ServiceRequest, ids)
    cache_service_requests()
def delete_requests_with_ids(ids):
    delete_requests_with_ids_task.delay(ids)


@capp.task
def update_professional_status_task(ids, approval):
    profs = get_all(Professional, ids=ids)
    for prof in profs:
        prof.approval = approval
    db.session.commit()
    cache_professionals()
def update_professional_status(ids, approval):
    update_professional_status_task.delay(ids, approval)


@capp.task
def update_customer_status_task(ids, status):
    customers = get_all(Customer, ids=ids)
    for customer in customers:
        customer.status = status
    db.session.commit()
    cache_customers()
def update_customer_status(ids, status):
    update_customer_status_task.delay(ids, status)


@capp.task
def update_customer_profile_task(id, editdata):
    customer = get_with_id(Customer, id)

    if customer.user.fullname != editdata.get('fullname'):
        customer.user.fullname = editdata.get('fullname')
    
    if customer.user.username != editdata.get('username'):
        customer.user.username = editdata.get('username')
    
    if customer.user.email != editdata.get('email'):
        customer.user.email = editdata.get('email')
    
    if customer.contact != editdata.get('contact'):
        customer.contact = editdata.get('contact')
    
    if customer.address != editdata.get('address'):
        customer.address = editdata.get('address')
    
    if customer.pincode != editdata.get('pincode'):
        customer.pincode = editdata.get('pincode')
    
    db.session.commit()
    cache_customers()
def update_customer_profile(id, editdata):
    update_customer_profile_task.delay(id, editdata)


@capp.task
def update_professional_profile_task(id, editdata):
    professional = get_with_id(Professional, id)
    if professional.user.fullname != editdata.get('fullname'):
        professional.user.fullname = editdata.get('fullname')
    if professional.user.username != editdata.get('username'):
        professional.user.username = editdata.get('username')
    if professional.user.email != editdata.get('email'):
        professional.user.email = editdata.get('email')
    if professional.experience != editdata.get('experience'):
        professional.experience = editdata.get('experience')
    if professional.description != editdata.get('description'):
        professional.description = editdata.get('description')
    if professional.contact != editdata.get('contact'):
        professional.contact = editdata.get('contact')
    if professional.address != editdata.get('address'):
        professional.address = editdata.get('address')
    if professional.pincode != editdata.get('pincode'):
        professional.pincode = editdata.get('pincode')
    db.session.commit()
    cache_professionals()
def update_professional_profile(id, editdata):
    update_professional_profile_task.delay(id, editdata)


@capp.task
def update_service_with_id_task(id, editdata):
    service = get_with_id(Service, id)
    service.name = editdata.get("name")
    service.description = editdata.get("description")
    service.price = editdata.get("price")
    service.timereq = editdata.get("timereq")
    db.session.commit()
    cache_services()
def update_service_with_id(id, editdata):
    update_service_with_id_task.delay(id, editdata)


@capp.task
def update_service_request_with_id_task(id, editdata):
    service_request = get_with_id(ServiceRequest, id)
    service_request.remarks = editdata.get("remarks")
    if not (editdata.get('completed') == 'In-Progess'):
        completed = datetime.strptime(editdata.get("completed"), "%Y-%m-%d %H:%M:%S")
        service_request.completed = completed
    db.session.commit()
    cache_service_requests()
def update_service_request_with_id(id, editdata):
    update_service_request_with_id_task.delay(id, editdata)


@capp.task
def close_service_request_with_id_task(id, editdata):
    service_request = get_with_id(ServiceRequest, id)
    service_request.rating = editdata.get('rating')
    service_request.remarks = editdata.get('remarks')
    service_request.status = "CLOSED"
    service_request.completed = datetime.now()
    db.session.commit()
    cache_service_requests()
def close_service_request_with_id(id, editdata):
    close_service_request_with_id_task.delay(id, editdata)


@capp.task
def accept_service_request_with_pid_task(id, editdata):
    service_request = get_with_id(ServiceRequest, id)
    accepting_professional = get_with_id(Professional, int(editdata.get('pid')))
    service_request.professional_id = accepting_professional.id
    service_request.status = "ASSIGNED"
    db.session.commit()
    cache_service_requests()
def accept_service_request_with_pid(id, editdata):
    accept_service_request_with_pid_task.delay(id, editdata)


@capp.task
def reject_service_request_with_pid_task(id, editdata):
    service_request = get_with_id(ServiceRequest, id)
    rejecting_professional = get_with_id(Professional, int(editdata.get('pid')))
    service_request.professional_id = rejecting_professional.id
    service_request.status = "REQUESTED"
    db.session.commit()
    cache_service_requests()
def reject_service_request_with_pid(id, editdata):
    reject_service_request_with_pid_task.delay(id, editdata)



def delete_with_id(model, pkid):
    sql = delete(model).where(model.id == pkid)
    db.session.execute(sql)
    db.session.commit()


@capp.task
def delete_service_with_id_task(id):
    delete_with_id(Service, id)
def delete_service_with_id(id):
    delete_service_with_id_task.delay(id)


@capp.task
def add_customer_user_task(user_data, cust_data):
    user = User(**user_data)
    customer = Customer(**cust_data)
    customer.user = user
    customer.user.password = gen_hash(user_data.get('password'))
    db.session.add(customer)
    db.session.commit()
    cache_users()
    cache_customers()
def add_customer_user(user_data, cust_data):
    add_customer_user_task.delay(user_data, cust_data)


@capp.task
def add_service_task(service_data):
    service = Service(**service_data)
    if service.service_exists():
        return { "added": False, "message": "Service Already Exists" }
    db.session.add(service)
    db.session.commit()
    cache_services()
    return { "added": True, "message": "Service Added Successfully" }
def add_service(service_data):
    add_service_task.delay(service_data)


@capp.task
def add_service_request_task(cid, sid, pid):
    service_request = ServiceRequest(
        customer_id = cid,
        service_id = sid,
        professional_id = pid
    )
    db.session.add(service_request)
    db.session.commit()
    
    professional_email = service_request.get_professional()['user']['email']
    customer_name = service_request.customer.user.fullname
    service_name = service_request.service.name
    send_email_to(professional_email, customer_name, service_name)
    
    cache_service_requests()
def add_service_request(cid, sid, pid):
    add_service_request_task.delay(cid, sid, pid)


@capp.task
def add_professional_user_task(user_data, prof_data):
    user = User(**user_data)
    professional = Professional(**prof_data)
    professional.user = user
    professional.user.password = gen_hash(user_data.get('password'))
    db.session.add(professional)
    db.session.commit()
    cache_users()
    cache_professionals()
def add_professional_user(user_data, prof_data):
    add_professional_user_task.delay(user_data, prof_data)







from models import Service, db, Professional, Customer, User, ServiceRequest
# from models import get_all, get_with_id, delete_with_id
from sqlalchemy import insert, select, delete
from fns import gen_hash
from datetime import datetime
from pprint import pprint
# from fns import cache_db

def create_dummy_services():
    services = [
        {
            "name": "Service A (db)",
            "price": 1000,
            "timereq": 10,
            "description": "Description for Service A (db)"
        },
        {
            "name": "Service B (db)",
            "price": 1200,
            "timereq": 20,
            "description": "Description for Service B (db)"
        },
        {
            "name": "Service C (db)",
            "price": 1400,
            "timereq": 30,
            "description": "Description for Service C (db)"
        },
        {
            "name": "Service D (db)",
            "price": 1600,
            "timereq": 40,
            "description": "Description for Service D (db)"
        }
    ]
    print()
    print("Creating Services:")

    for kw in services:
        service = Service(**kw)
        db.session.add(service)
    db.session.commit()


def create_dummy_profs():
    hashedone = gen_hash("97532468")
    profs = [
        {
            "user": {
                "fullname": "Professional A",
                "username": "profA",
                "email": "profa@gmail.com",
                "password": hashedone,
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543211",
                "address": "Address for A",
                "pincode": "110025",
                "experience": 5,
                "description": "Description for A",
                "service_id": 1
            }
        },
        {
            "user": {
                "fullname": "Professional B",
                "username": "profB",
                "email": "profb@gmail.com",
                "password": hashedone,
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543212",
                "address": "Address for B",
                "pincode": "110026",
                "experience": 6,
                "description": "Description for B",
                "service_id": 2,
            }
        },
        {
            "user": {
                "fullname": "Professional C",
                "username": "profC",
                "email": "profc@gmail.com",
                "password": hashedone,
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543213",
                "address": "Address for C",
                "pincode": "110027",
                "experience": 7,
                "description": "Description for C",
                "service_id": 3,
                "approval": "APPROVED",
            }
        },
        {
            "user": {
                "fullname": "Professional D",
                "username": "profD",
                "email": "profd@gmail.com",
                "password": hashedone,
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543214",
                "address": "Address for D",
                "pincode": "110028",
                "experience": 8,
                "description": "Description for D",
                "service_id": 4,
                "approval": "APPROVED",
            }
        }
    ]
    print()
    print("Creating Professionals:")

    for kw in profs:
        user = User(**kw['user'])
        prof = Professional(**kw['prof'])
        prof.user = user
        db.session.add(prof)
    db.session.commit()


def create_dummy_custs():
    hashedone = gen_hash("97532469")
    custs = [
        {
            "user": {
                "fullname": "Customer A",
                "username": "custA",
                "email": "custa@gmail.com",
                "password": hashedone,
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543210",
                "address": "Address for Customer A",
                "pincode": "110025",
            }
        },
        {
            "user": {
                "fullname": "Customer B",
                "username": "custB",
                "email": "custb@gmail.com",
                "password": hashedone,
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543220",
                "address": "Address for Customer B",
                "pincode": "110026",
            }
        },
        {
            "user": {
                "fullname": "Customer C",
                "username": "custC",
                "email": "custc@gmail.com",
                "password": hashedone,
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543230",
                "address": "Address for Customer C",
                "pincode": "110027",
            }
        },
        {
            "user": {
                "fullname": "Customer D",
                "username": "custD",
                "email": "custd@gmail.com",
                "password": hashedone,
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543240",
                "address": "Address for Customer D",
                "pincode": "110028",
            }
        },
        {
            "user": {
                "fullname": "Customer E",
                "username": "custE",
                "email": "custe@gmail.com",
                "password": hashedone,
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543250",
                "address": "Address for Customer E",
                "pincode": "110029",
                "status": "BLOCKED",
            }
        },
        {
            "user": {
                "fullname": "Customer F",
                "username": "custF",
                "email": "custf@gmail.com",
                "password": hashedone,
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543260",
                "address": "Address for Customer F",
                "pincode": "110030",
                "status": "BLOCKED",
            }
        },
    ]
    print()
    print("Creating Customers:")

    for kw in custs:
        user = User(**kw['user'])
        cust = Customer(**kw['cust'])
        cust.user = user
        db.session.add(cust)
    db.session.commit()

def create_dummy_admin():
    hashedone = gen_hash("97532460")
    admin = {
        "fullname": "Admin",
        "username": "admin",
        "email": "admin@hhs.org",
        "password": hashedone,
        "role": "ADMIN",
    }
    print()
    print("Creating Admin:")

    admin = User(**admin)
    db.session.add(admin)
    db.session.commit()

def create_dummy_requests():
    requests = [
        {
            "service_id": 1,
            "customer_id": 1,
        },
        {
            "service_id": 1,
            "customer_id": 1,
        },
        {
            "service_id": 1,
            "customer_id": 2,
        },
        {
            "service_id": 1,
            "customer_id": 3,
        },
        {
            "service_id": 1,
            "customer_id": 4,
        },
        {
            "service_id": 1,
            "customer_id": 1,
            "professional_id": 1,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "customer_id": 1,
            "professional_id": 2,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "customer_id": 3,
            "professional_id": 1,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "customer_id": 4,
            "professional_id": 1,
            "status": "ASSIGNED",
        },
        {
            "service_id": 3,
            "customer_id": 3,
            "professional_id": 3,
            "status": "ASSIGNED",
        },
        {
            "service_id": 4,
            "customer_id": 4,
            "professional_id": 4,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 1,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 2,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 5,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 6,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        }
    ]
    print()
    print("Creating Service Requests:")
    for kw in requests:
        request = ServiceRequest(**kw)
        db.session.add(request)
    db.session.commit()


def get_all_services():
    services = get_all(Service)
    print()
    print("Getting All Services:")
    for service in services:
        print(f"{service.id}, {service.name}, {service.created}")

def get_all_profs():
    profs = get_all(Professional)
    print()
    print("Getting All Professionals:")
    for prof in profs:
        print(f"{prof.id}, {prof.service.name}, {prof.user.fullname}, {prof.approval}, {prof.user.role}, {prof.created}")

def get_all_custs():
    custs = get_all(Customer)
    print()
    print("Getting All Customers:")
    for cust in custs:
        print(f"{cust.id}, {cust.user.fullname}, {cust.user.role}, {cust.created}")

def get_admin():
    sql = select(User).filter_by(fullname="Admin")
    admin = db.session.scalars(sql).first()
    print()
    print("Getting Admin:")
    if admin:
        print(f"{admin.id}, {admin.fullname}, {admin.email}, {admin.role}")

def get_all_users():
    users = get_all(User)
    print()
    print("Getting All Users:")
    for user in users:
        print(f"{user.id}, {user.fullname}, {user.username}, {user.email}")

def get_all_requests():
    requests = get_all(ServiceRequest)
    print()
    print("Getting All Service Requests:")
    for req in requests:
        print(f"{req.id}, {req.service_id}, {req.customer.id}, {req.professional_id}, {req.status}")



def rm_all_services():
    print()
    print("Removing All Services:")
    sql = delete(Service)
    db.session.execute(sql)
    db.session.commit()


def rm_all_profs():
    print()
    print("Removing All Professionals:")
    sql = delete(Professional)
    db.session.execute(sql)
    db.session.commit()


def rm_all_custs():
    print()
    print("Removing All Customers:")
    sql = delete(Customer)
    db.session.execute(sql)
    db.session.commit()


def rm_admin():
    print()
    print("Removing Admin:")
    sql = delete(User).filter_by(username="admin")
    db.session.execute(sql)
    db.session.commit()

def rm_all_users():
    print()
    print("Removing All Users:")
    sql = delete(User)
    db.session.execute(sql)
    db.session.commit()

def rm_all_requests():
    print()
    print("Removing All Service Requests:")
    sql = delete(ServiceRequest)
    db.session.execute(sql)
    db.session.commit()

def create_dummy_data():
    create_dummy_admin()
    create_dummy_services()
    create_dummy_profs()
    create_dummy_custs()
    create_dummy_requests()

def get_data():
    get_all_services()
    get_all_profs()
    get_all_custs()
    get_admin()
    get_all_users()
    get_all_requests()

def rm_data():
    rm_all_services()
    rm_all_profs()
    rm_all_custs()
    rm_admin()
    rm_all_users()
    rm_all_requests()

# create_dummy_data()
# rm_data()
# get_data()

##############################################################################3
# cache_db()
from redis import Redis
import json

redis_client = Redis(decode_responses=True)

def get_all(model, ids=None):
    if ids:
        sql = select(model).where(model.id.in_(ids)).order_by(model.id)
    else:
        sql = select(model).order_by(model.id)
    results = db.session.scalars(sql)
    return results

def get_all_professionals(ids=None):
    if redis_client.exists("PROFESSIONAL_ALL") > 0:
        print("CACHE EXISTS HERE")
        professional_all_dict_list = json.loads(redis_client.get("PROFESSIONAL_ALL"))
        return professional_all_dict_list

    print("NO CACHE EXISTS")
    professional_all = get_all(Professional, ids=ids)
    professional_all_dict_list = [professional.to_dict() for professional in professional_all]
    redis_client.setex("PROFESSIONAL_ALL", 10, json.dumps(professional_all_dict_list))
    return professional_all_dict_list

def get_professional_with_id(id):
    professional_all_dict_list = get_all_professionals()
    def extract_professional(prof_data):
        return prof_data['id'] == id
    professional_dict = list(filter(extract_professional, professional_all_dict_list))[0]
    return professional_dict

pprint(get_professional_with_id(2))
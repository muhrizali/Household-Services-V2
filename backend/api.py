from apps import api, app
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from fns import *
# from time import sleep

# Caching Database before anything
cache_db()

# core views
@app.route("/core/test", methods=["GET", "POST"])
def test():
    return { "message": "Hello Mom, This is flask core" }

@app.route("/core/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    try:
        if email and password:
            user = get_user_with_creds(email, password)        
        if user:
            return login_user(user)
        else:
            return { "logged_in": False, "message": "Wrong Email/Password" }, 401
    except Exception as e:
        return { "logged_in": False, "message": f"Error: {str(e)}" }, 401


@app.route("/core/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_username = get_jwt_identity()
    user = get_user_with_username(current_user_username)
    if user.role == "CUSTOMER":
        return {
            "logged_in": True,
            "id": user.get_customer().id,
            "user": user.email, 
            "role": "CUSTOMER", 
        }
    elif user.role == "PROFESSIONAL":
        return {
            "logged_in": True,
            "id": user.get_prof().id,
            "user": user.email, 
            "role": "PROFESSIONAL", 
        }
    elif user.role == "ADMIN":
        return {
            "logged_in": True,
            "user": user.email, 
            "role": "ADMIN",
        }


# API resources

# for logins
class LoginAPI(Resource):
    
    def get(self):
        # req = request.args
        # if req.get("check_protect"):
        #     current_user = get_jwt_identity()
        #     return { "logged_in": True, "user_id": current_user }
        pass
    
    def post(self):
        # data = request.json
        # email = data.get("email")
        # password = data.get("password")
        # try:
        #     if email and password:
        #         user = get_user_with_creds(email, password)        
        #     if user:
        #         return login(user)
        #     else:
        #         return { "logged_in": False, "message": "Wrong Email/Password" }, 401
        # except:
        #     return { "logged_in": True, "message": "Something Went Wrong" }, 401
        pass



# professionals
class ProfessionalAPI(Resource):
    def get(self):
        req = request.args
        if req.get("id"):
            professional = get_professional_with_id(id = int(req.get("id")))
            if professional:
                return jsonify({ "professional": professional, "found": True })
            else:
                return jsonify({ "found": False })

        if req.get('sid'):
            professionals = get_all_professionals_with_sid(sid = int(req.get('sid')))
            if professionals:
                return jsonify({ 'professionals': professionals, 'found': True })
            else:
                return jsonify({ "found": False })

        if req.get("ids"):
            professionals = get_all_professionals(ids = req.getlist("ids"))
            if professionals:
                return jsonify({ "professionals": professionals, "found": True })
            else:
                return jsonify({ "found": False })
        professionals = get_all_professionals()
        return jsonify({ "professionals": professionals })
    
    def post(self):
        new_user = request.get_json()
        # print(new_user)
        try:
            add_professional_user(new_user['user'], new_user['professional'])
            resp = { "message": "Professional Successfully Added" }
            return resp
        except:
            resp = { "message": "Error While Registering User" }
            return resp, 400
    
    def put(self):
        req = request.get_json()
        if req.get("approve_selected"):
            update_professional_status(ids=req.get("ids"), approval="APPROVED")
            return jsonify({ "edited": True })
        
        if req.get("reject_selected"):
            update_professional_status(ids=req.get("ids"), approval="REJECTED")
            return jsonify({ "edited": True })
        
        if req.get('edit_profile'):
            update_professional_profile(id=int(req.get('id')), editdata=req)
            return jsonify({ 'edited': True })
                


class CustomerAPI(Resource):
    # get all users
    def get(self):
        req = request.args
        if req.get("id"):
            customer = get_customer_with_id(id = int(req.get("id")))
            if customer:
                return jsonify({ "customer": customer, "found": True })
            else:
                return jsonify({ "found": False })
        customers = get_all_customers()
        return jsonify({ "customers": customers })

    # adding new customer
    def post(self):
        new_user = request.get_json()
        try:
            add_customer_user(new_user.get('user'), new_user.get('customer'))
            resp = { "message": "Customer Successfully Added" }
            return resp
        except:
            resp = { "message": "Error While Registering User" }
            return resp, 400

    def put(self):
        req = request.get_json()
        if req.get("activate_selected"):
            update_customer_status(ids=req.get('ids'), status="ACTIVE")
            return jsonify({ "edited": True })
        
        if req.get("block_selected"):
            update_customer_status(ids=req.get("ids"), status="BLOCKED")
            return jsonify({ "edited": True })
        
        if req.get('edit_profile'):
            update_customer_profile(id=int(req.get('id')), editdata=req)
            return jsonify({ 'edited': True })

# services
class ServiceAPI(Resource):
    def get(self):
        req = request.args
        if req.get("id"):
            service = get_service_with_id(id = int(req.get("id")))
            if service:
                return jsonify({ "service": service, "found": True })
            else:
                return jsonify({ "found": False })
        if req.get("ids"):
            services = get_all_services(ids = req.get("ids"))
            return jsonify({ "services": services, 'found': True })
        services = get_all_services()
        return jsonify({ "services": services, 'found': True })
    
    def post(self):
        new_service_data = request.get_json()
        try:
            return jsonify(add_service(new_service_data))
        except:
            return { "added": False, "message": "Error While Adding Service" }, 400
    
    def delete(self):
        req = request.args
        if req.get("id"):
            delete_services_with_ids([req.get("id")])
            return jsonify({ "deleted": True })
        elif req.get("ids"):
            delete_services_with_ids(req.getlist("ids"))
            return jsonify({ "deleted": True })
    
    def put(self):
        req = request.get_json()
        try:
            update_service_with_id(req.get("id"), req)
            return jsonify({ "edited": True })
        except:
            return jsonify({ "edited": False })
        
        


# service requests
class ServiceRequestAPI(Resource):
    def get(self):
        req = request.args
        if req.get("id"):
            service_request = get_request_with_id(id = int(req.get("id")))
            if service_request:
                return jsonify({ "service_request": service_request, "found": True })
            else:
                return jsonify({ "found": False })

        if req.get("cid"):
            service_requests = get_all_requests_with_cid(cid = int(req.get('cid')))
            if service_requests:
                return jsonify({ "found": True, "requests": service_requests })
            else:
                return jsonify({ 'found': False })
        
        if req.get("assigned_requests"):
            service_requests = get_assigned_requests_with_pid(pid = int(req.get('pid')))
            if service_requests:
                return jsonify({ 'found': True, 'requests': service_requests })
            else:
                return jsonify({ 'found': False })

        if req.get("new_requests"):
            service_requests = get_new_requests_with_pid(pid = int(req.get('pid')))
            if service_requests:
                return jsonify({ 'found': True, 'requests': service_requests })
            else:
                return jsonify({ 'found': False })

        if req.get("closed_requests"):
            service_requests = get_closed_requests_with_pid(pid = int(req.get('pid')))
            if service_requests:
                return jsonify({ 'found': True, 'requests': service_requests })
            else:
                return jsonify({ 'found': False })

        # if req.get("search_all_requests"):
        #     service_requests = get_closed_requests_with_pid(pid = int(req.get('pid')))
        #     if service_requests:
        #         return jsonify({ 'found': True, 'requests': service_requests })
        #     else:
        #         return jsonify({ 'found': False })

        
        service_requests = get_all_requests()
        if service_requests:
            return jsonify({ "found": True, "requests": service_requests })
        else:
            return jsonify({ 'found': False })
        
    def post(self):
        new_service_request_data = request.get_json()
        if new_service_request_data:
            add_service_request(
                new_service_request_data.get('cid'), 
                new_service_request_data.get('sid'), 
                new_service_request_data.get('pid')
            )
            return jsonify({ 'added': True })
        else:
            return jsonify({ 'added': False }), 401



    def put(self):
        req = request.get_json()

        if req.get('edit_request'):
            update_service_request_with_id(id=int(req.get("id")), editdata=req)
            return jsonify({ "edited": True })
        
        if req.get('close_request'):
            close_service_request_with_id(id=int(req.get('id')), editdata=req)
            return jsonify({ "edited": True })
        
        if req.get('accept_request'):
            accept_service_request_with_pid(id=int(req.get('id')), editdata=req)
            return jsonify({ 'edited': True })

        if req.get('reject_request'):
            reject_service_request_with_pid(id=int(req.get('id')), editdata=req)
            return jsonify({ 'edited': True })




    def delete(self):
        req = request.args
        
        if req.get("id"):
            delete_requests_with_ids([req.get("id")])
            return jsonify({ "deleted": True })
        
        if req.get("ids"):
            delete_requests_with_ids(req.getlist("ids"))
            return jsonify({ "deleted": True })


class SearchAPI(Resource):
    def get(self):
        reqs = request.args
        parameter = reqs.get("parameter")
        query = reqs.get("query")

        if parameter.startswith("professional"):
            professionals = search_objects(parameter, query)
            results = [professional.to_dict() for professional in professionals]
            return jsonify({ "found": True, "type": "PROFESSIONAL", "results": results })
        
        elif parameter.startswith("customer"):
            customers = search_objects(parameter, query)
            results = [customer.to_dict() for customer in customers]
            return jsonify({ "found": True, "type": "CUSTOMER", "results": results })
        
        elif parameter.startswith("service"):
            services = search_objects(parameter, query)
            results = [service.to_dict() for service in services]
            return jsonify({ "found": True, "type": "SERVICE", "results": results })
        
        elif parameter.startswith("request") and reqs.get('pid'):
            service_requests = search_request_objects_with_pid(int(reqs.get('pid')), parameter, query)
            results = [service_request.to_dict() for service_request in service_requests]
            return jsonify({ "found": True, "type": "SERVICE_REQUEST", "results": results })

        elif parameter.startswith("request"):
            service_requests = search_objects(parameter, query)
            results = [service_request.to_dict() for service_request in service_requests]
            return jsonify({ "found": True, "type": "SERVICE_REQUEST", "results": results })


        

        

# for development testing
class TestAPI(Resource):
    def get(self):
        # sleep(5.0)
        test_dict = {
            "name": "Muhriz Ali",
            "purpose": "Testing Purpose"
        }
        return jsonify(test_dict)
    
    def post(self):
        req = request.json
        test_dict = {
            "YourName": req["name"],
            "Purpose": "POST successfully reached"
        }
        return jsonify(test_dict)

# API routes
# api.add_resource(LoginAPI, "/api/login")

api.add_resource(ProfessionalAPI, "/api/professional")
api.add_resource(CustomerAPI, "/api/customer")
api.add_resource(ServiceAPI, "/api/service")
api.add_resource(ServiceRequestAPI, "/api/request")

api.add_resource(SearchAPI, "/api/search")

# testing APIs
api.add_resource(TestAPI, "/api/test")


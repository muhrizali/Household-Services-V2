from apps import api
from flask import request, jsonify
from flask_restful import Resource
from fns import *
from time import sleep


# API resources

# for logins
class LoginAPI(Resource):
    def get(self):
        return { "Hello": "Mom" }
    
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        try:
            if email and password:
                user = get_user_with_creds(email, password)        
            if user:
                # return user.to_dict()
                return login(user)
            else:
                return { "message": "Wrong Email or Password" }, 401
        except:
            return { "message": "Something Went Wrong" }, 401

# for cookies sessions
class SessionAPI(Resource):
    def get(self):
        data = request.json
        return check_session()
        # user = get_user_with_id(data.get('id'))


# professionals
class ProfessionalAPI(Resource):
    def get(self):
        req = request.args
        if req.get("id"):
            professional = get_professional_with_id(id = req.get("id"))
            if professional:
                return jsonify({ "professional": professional.to_dict(), "found": True })
            else:
                return jsonify({ "found": False })
        professionals = get_all_professionals()
        data = [professional.to_dict() for professional in professionals]
        return jsonify({ "professionals": data })
    
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
                


class CustomerAPI(Resource):
    # get all users
    def get(self):
        req = request.args
        if req.get("id"):
            customer = get_customer_with_id(id = req["id"])
            if customer:
                return jsonify({ "customer": customer.to_dict(), "found": True })
            else:
                return jsonify({ "found": False })
        customers = get_all_customers()
        data = [customer.to_dict() for customer in customers]
        return jsonify({ "customers": data })

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
            update_customer_status(ids=req.get("ids"), status="ACTIVE")
            return jsonify({ "edited": True })
        
        if req.get("block_selected"):
            update_customer_status(ids=req.get("ids"), status="BLOCKED")
            return jsonify({ "edited": True })

# services
class ServiceAPI(Resource):
    def get(self):
        req = request.args
        if req.get("id"):
            service = get_service_with_id(id = req.get("id"))
            if service:
                return jsonify({ "service": service.to_dict(), "found": True })
            else:
                return jsonify({ "found": False })
        if req.get("ids"):
            services = get_all_services(ids = req.get("ids"))
            if services:
                data = [service.to_dict() for service in services]
                return jsonify({ "services": data })
        services = get_all_services()
        if services:
            data = [service.to_dict() for service in services]
            return jsonify({ "services": data })
    
    def post(self):
        new_service_data = request.json
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
        req = request.json
        try:
            update_service_with_id(req.get("id"), req)
            return jsonify({ "edited": True })
        except:
            return jsonify({ "edited": False })
        
        


# service requests
class ServiceRequestAPI(Resource):
    def get(self):
        reqs = request.args
        if reqs.get("id"):
            service_request = get_request_with_id(id = reqs.get("id"))
            if service_request:
                return jsonify({ "service_request": service_request.to_dict(), "found": True })
            return jsonify({ "found": False })
        service_requests = get_all_requests()
        data = [service_request.to_dict() for service_request in service_requests]
        return jsonify({ "requests": data })

    def delete(self):
        req = request.args
        if req.get("id"):
            delete_requests_with_ids([req.get("id")])
            return jsonify({ "deleted": True })
        elif req.get("ids"):
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
api.add_resource(LoginAPI, "/api/login")
api.add_resource(SessionAPI, "/api/check_session")

api.add_resource(ProfessionalAPI, "/api/professional")
api.add_resource(CustomerAPI, "/api/customer")
api.add_resource(ServiceAPI, "/api/service")
api.add_resource(ServiceRequestAPI, "/api/request")

api.add_resource(SearchAPI, "/api/search")

# testing APIs
api.add_resource(TestAPI, "/api/test")


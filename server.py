#flask --app server run

from flask import Flask
from flask import json, jsonify, request
import json


with open("vehicle.json") as vehicleJson:
   vehicle_data = json.load(vehicleJson)

with open ("customer.json") as customerJson:
    customer_data = json.load(customerJson)

vehicle_id = len(vehicle_data) + 1
customer_id = len(customer_data) + 1

app = Flask(__name__)

@app.route("/")
def landing_page():
    return "landing page"
    
@app.route("/customers")
def customers():
    return customer_data

@app.route("/vehicles")
def vehicles():
    return vehicle_data

@app.route("/vehicles/colour/<colour>", methods=["GET"])
def get_colour(colour):

    matching_vehicles = [v for v in vehicle_data if v["colour"] == colour]

    if matching_vehicles:
        return jsonify(matching_vehicles)
     
    return "not found", 404

@app.route("/vehicles/make/<make>", methods=["GET"])
def get_make(make):

    matching_vehicles = [v for v in vehicle_data if v["make"] == make]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/year/<year>", methods=["GET"])
def get_year(year):

    matching_vehicles = [v for v in vehicle_data if v["year"] == year]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/vrm/<vrm>", methods=["GET"])
def get_vrm(vrm):

    matching_vehicles = [v for v in vehicle_data if v["vrm"] == vrm]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/category/<category>", methods=["GET"])
def get_category(category):

    matching_vehicles = [v for v in vehicle_data if v["category"] == category]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/numberSeats/<numberSeats>", methods=["GET"])
def get_numberSeats(numberSeats):

    matching_vehicles = [v for v in vehicle_data if v["numberSeats"] == numberSeats]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/dayRate/<dayRate>", methods=["GET"])
def get_dayRate(dayRate):

    matching_vehicles = [v for v in vehicle_data if v["dayRate"] == dayRate]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/branch/<branch>", methods=["GET"])
def get_branch(branch):

    matching_vehicles = [v for v in vehicle_data if v["branch"] == branch]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/status/<status>", methods=["GET"])
def get_status(status):

    matching_vehicles = [v for v in vehicle_data if v["status"] == status]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/model/<model>", methods=["GET"])
def get_model(model):

    matching_vehicles = [v for v in vehicle_data if v["model"] == model]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles/<make>/<colour>", methods=["GET"])
def get_make_colour(make, colour):
    matching_vehicles = [v for v in vehicle_data if v["make"] == make and v["colour"] == colour]

    if matching_vehicles:
        return jsonify(matching_vehicles) 
    
    return "not found", 404

@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    global vehicle_id

    try:
        new_vehicle = request.get_json()  
         
        if not new_vehicle:
            return jsonify({"error": "Invalid JSON data in request body"}), 400

        if "make" in new_vehicle and "model" in new_vehicle and "colour" in new_vehicle and "vin" and "year" in new_vehicle and "vrm" in new_vehicle and "category" and "numberSeats" in new_vehicle and "dayRate" in new_vehicle and "status" in new_vehicle and "fuelEconomy" in new_vehicle and "branch" in new_vehicle:
            
            new_vehicle["id"] = vehicle_id
            vehicle_id += 1

            vehicle_data.append(new_vehicle)
            return jsonify({"message": "Vehicle added successfully"}), 200
        
        else:
            return jsonify({"error": "Invalid vehicle data"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/vehicles/<vrm>", methods=["DELETE"])
def remove_vehicle(vrm):
    global vehicle_data  

    vehicle_to_delete = next((i for i, v in enumerate(vehicle_data) if v["vrm"] == vrm), None) # Find the index of the vehicle to remove

    if vehicle_to_delete is not None:
        removed_vehicle = vehicle_data.pop(vehicle_to_delete)  # Removes the vehicle

        return jsonify({"message": "Vehicle removed successfully", "removed_vehicle": removed_vehicle}), 200
    
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    
@app.route("/vehicles/<vrm>/status", methods=["PATCH"])
def change_vehicle_color(vrm):

    global vehicle_data  

    updated_status = request.json.get("status", "").strip()  # Get the new status from the request


    status_to_update = next((i for i, v in enumerate(vehicle_data) if v["vrm"] == vrm), None) # Finds the index of the vehicle to update

    if status_to_update is not None:
        vehicle_data[status_to_update]["status"] = updated_status

        return jsonify({"message": "The vehicle has been rented"}), 200
    
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    

@app.route("/customers/country/<country>", methods=["GET"])
def get_country(country):

    matching_customers = [c for c in customer_data if c["country"] == country]

    if matching_customers:
        return jsonify(matching_customers) 
    
    return "not found", 404


@app.route("/customers", methods=["POST"])
def add_customer():
    global customer_id

    try:
        new_customer = request.get_json()  
         
        if not new_customer:
            return jsonify({"error": "Invalid JSON data in request body"}), 400

        if "first_name" in new_customer and "last_name" in new_customer and "dob" in new_customer and "gender" in new_customer and "email" in new_customer and "address" in new_customer and "city" in new_customer and "country" in new_customer and "drivingLicenseNumber" in new_customer and "passportNumber" in new_customer and "LicenseRetrictions" in new_customer and "ip_address_v4" in new_customer and "ip_address_v6" in new_customer:
            
            new_customer["id"] = customer_id
            customer_id += 1

            customer_data.append(new_customer)
            return jsonify({"message": "Customer added successfully"}), 200
        
        else:
            return jsonify({"error": "Invalid customer data"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/customers/<passportNumber>", methods=["DELETE"])
def remove_customer(passportNumber):
    global customer_data  

    customer_to_delete = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Find the index of the customer to remove

    if customer_to_delete is not None:
        removed_customer = customer_data.pop(customer_to_delete)  # Removes the customer

        return jsonify({"message": "Customer removed successfully", "removed_customer": removed_customer}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404


@app.route("/customers/<passportNumber>/country", methods=["PATCH"])
def change_customer_color(passportNumber):

    global customer_data  

    updated_country = request.json.get("country", "").strip()  # Get the new country from the request


    country_to_update = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Finds the index of the customer to update

    if country_to_update is not None:
        customer_data[country_to_update]["country"] = updated_country

        return jsonify({"message": "The customer's country of residence has been changed"}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route("/customers/<passportNumber>/city", methods=["PATCH"])
def change_customer_city(passportNumber):

    global customer_data  

    updated_city = request.json.get("city", "").strip()  # Get the new city from the request


    city_to_update = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Finds the index of the customer to update

    if city_to_update is not None:
        customer_data[city_to_update]["city"] = updated_city

        return jsonify({"message": "The customer's city of residence has been changed"}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404
    
@app.route("/customers/<passportNumber>/address", methods=["PATCH"])
def change_customer_address(passportNumber):

    global customer_data  

    updated_address = request.json.get("address", "").strip()  # Get the new address from the request


    address_to_update = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Finds the index of the customer to update

    if address_to_update is not None:
        customer_data[address_to_update]["address"] = updated_address

        return jsonify({"message": "The customer's address of residence has been changed"}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route("/customers/<passportNumber>/email", methods=["PATCH"])
def change_customer_email(passportNumber):

    global customer_data  

    updated_email = request.json.get("email", "").strip()  # Get the new email from the request


    email_to_update = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Finds the index of the customer to update

    if email_to_update is not None:
        customer_data[email_to_update]["email"] = updated_email

        return jsonify({"message": "The customer's email has been changed"}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404

app.run()
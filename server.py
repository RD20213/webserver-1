#flask --app server run

from flask import Flask, json, jsonify, request


with open("vehicle.json") as vehicleJson:
   vehicle_data = json.load(vehicleJson) #Loads the vehicle data from json

with open ("customer.json") as customerJson:
    customer_data = json.load(customerJson) #Loads the customer's data from json

# create functions to write changes back to original files, one for vehicles and one for customer
def save_vehicles():
    with open("vehicle.json", "w") as vehicleJson:
        vehicleJson.write(vehicle_data)
    vehicleJson.close()


def save_customers():
    with open("vehicle.json", "w") as customerJson:
        customerJson.write(customer_data)
    customerJson.close()
   
vehicle_id = len(vehicle_data) + 1
customer_id = len(customer_data) + 1  #setting id values for both vehicle and customer, so when a record is added, it wil auto increment

app = Flask(__name__)


@app.route("/")
def landing_page():
    return "landing page"
    
@app.route("/customers")
def customers():
    return customer_data    #returns all the customers and their data

@app.route("/vehicles")
def vehicles():
    return vehicle_data #returns all the vehicles and data

@app.route("/vehicles/colour/<colour>", methods=["GET"])
def get_colour(colour): #GET for the key 'colour'

    matching_vehicles = [v for v in vehicle_data if v["colour"] == colour] #checking if the coulour input in the url is present in any of the vechile records

    if matching_vehicles:
        return jsonify(matching_vehicles)   #returns the information for all vehicles with the specified colour
     
    return "not found", 404

@app.route("/vehicles/make/<make>", methods=["GET"])
def get_make(make):

    matching_vehicles = [v for v in vehicle_data if v["make"] == make] #checking if the "make" input in the url is present in any of the vechile records

    if matching_vehicles:
        return jsonify(matching_vehicles)   #returns the information for all vehicles with the specified make
    
    return "not found", 404

@app.route("/vehicles/year/<year>", methods=["GET"])
def get_year(year):

    matching_vehicles = [v for v in vehicle_data if v["year"] == year] #checking if the "year" input in the url is present in any of the vechile records

    if matching_vehicles:
        return jsonify(matching_vehicles)  #Returns the information for all vehicles with the specified year
    
    return "not found", 404

@app.route("/vehicles/vrm/<vrm>", methods=["GET"])
def get_vrm(vrm):

    matching_vehicles = [v for v in vehicle_data if v["vrm"] == vrm] #checking if the vrm input in the url is present in any of the vechile records

    if matching_vehicles:
        return jsonify(matching_vehicles) #Returns the information of the vehicle with a matching vrm
    
    return "not found", 404

@app.route("/vehicles/category/<category>", methods=["GET"])
def get_category(category):

    matching_vehicles = [v for v in vehicle_data if v["category"] == category] #checking if the category input in the url is present in any of the vehicle records

    if matching_vehicles:
        return jsonify(matching_vehicles) #Returns the information for all vehicles with the specified category
    
    return "not found", 404

@app.route("/vehicles/numberSeats/<numberSeats>", methods=["GET"])
def get_numberSeats(numberSeats):

    matching_vehicles = [v for v in vehicle_data if v["numberSeats"] == numberSeats] #checking if the No. seats input in the url is present in any of the vehicle records

    if matching_vehicles:
        return jsonify(matching_vehicles) #Returns the information for all vehicles with the specified No. seats
    
    return "not found", 404

@app.route("/vehicles/dayRate/<dayRate>", methods=["GET"])
def get_dayRate(dayRate):

    matching_vehicles = [v for v in vehicle_data if v["dayRate"] == dayRate] #checking if the day rate input in the url is present in any of the vehicle records

    if matching_vehicles:
        return jsonify(matching_vehicles) #Returns the information for all vehicles with the specified day rate
    
    return "not found", 404

@app.route("/vehicles/branch/<branch>", methods=["GET"])
def get_branch(branch):

    matching_vehicles = [v for v in vehicle_data if v["branch"] == branch] #checking if the bramch input in the url is present in any of the vehicle records

    if matching_vehicles:
        return jsonify(matching_vehicles) #Returns the information for all vehicles that are held in the specified branch
    
    return "not found", 404

@app.route("/vehicles/status/<status>", methods=["GET"])
def get_status(status):

    matching_vehicles = [v for v in vehicle_data if v["status"] == status] #checking if a vehicle is rented or available, or has some other status e.g. damaged
   
    if matching_vehicles:
        return jsonify(matching_vehicles) #returns any relevant vehicle records that match the specified status
    
    return "not found", 404

@app.route("/vehicles/model/<model>", methods=["GET"])
def get_model(model):

    matching_vehicles = [v for v in vehicle_data if v["model"] == model] #checking if the vehicle model input in the url is present in any of the vehicle records

    if matching_vehicles:
        return jsonify(matching_vehicles) #returns any relevant vehicle records that match the specified model type
    
    return "not found", 404

@app.route("/vehicles/<make>/<colour>", methods=["GET"])
def get_make_colour(make, colour):
    matching_vehicles = [v for v in vehicle_data if v["make"] == make and v["colour"] == colour] #checking if the vehicle make and colour input in the url is present in any of the vehicle records

    if matching_vehicles:
        return jsonify(matching_vehicles) #returns any relevant vehicle records that match the specified make and colour
    
    return "not found", 404

@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    global vehicle_id #taking that initial vehicle Id 

    try:
        new_vehicle = request.get_json()  
         
        if not new_vehicle:
            return jsonify({"error": "Invalid JSON data in request body"}), 400

        if "make" in new_vehicle and "model" in new_vehicle and "colour" in new_vehicle and "vin" and "year" in new_vehicle and "vrm" in new_vehicle and "category" and "numberSeats" in new_vehicle and "dayRate" in new_vehicle and "status" in new_vehicle and "fuelEconomy" in new_vehicle and "branch" in new_vehicle: #Ensures that the vehicle record input has all the necessary values to be valid
            
            new_vehicle["id"] = vehicle_id
            vehicle_id += 1 #increments the vehicle_id by 1 

            vehicle_data.append(new_vehicle) #Adds the new vehicle record to the json
            save_vehicles()
            return jsonify({"message": "Vehicle added successfully"}), 200
        
        else:
            return jsonify({"error": "Invalid vehicle data"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/vehicles/<vrm>", methods=["DELETE"])
def remove_vehicle(vrm):
    global vehicle_data  

    vehicle_to_delete = next((i for i, v in enumerate(vehicle_data) if v["vrm"] == vrm), None) # Find the index of the vehicle to remove by the vrm input

    if vehicle_to_delete is not None:
        removed_vehicle = vehicle_data.pop(vehicle_to_delete)  # Removes the vehicle
        save_vehicles()
        return jsonify({"message": "Vehicle removed successfully", "removed_vehicle": removed_vehicle}), 200
    
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    
@app.route("/vehicles/<vrm>/status", methods=["PATCH"])
def change_vehicle_color(vrm):

    global vehicle_data  

    updated_status = request.json.get("status", "").strip()  # Get the new status from the request


    status_to_update = next((i for i, v in enumerate(vehicle_data) if v["vrm"] == vrm), None) # Finds the index of the vehicle to update

    if status_to_update is not None:
        vehicle_data[status_to_update]["status"] = updated_status #sets the staus to rented
        save_vehicles()
        return jsonify({"message": "The vehicle has been rented"}), 200
    
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    

@app.route("/customers/country/<country>", methods=["GET"])
def get_country(country):

    matching_customers = [c for c in customer_data if c["country"] == country] #returns all the customers from the country input

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

        if "first_name" in new_customer and "last_name" in new_customer and "dob" in new_customer and "gender" in new_customer and "email" in new_customer and "address" in new_customer and "city" in new_customer and "country" in new_customer and "drivingLicenseNumber" in new_customer and "passportNumber" in new_customer and "LicenseRetrictions" in new_customer and "ip_address_v4" in new_customer and "ip_address_v6" in new_customer: #Ensures that the person record input has all the necessary values to be valid
            
            new_customer["id"] = customer_id
            customer_id += 1 #increments the customer_id by 1

            customer_data.append(new_customer)
            save_customers()
            return jsonify({"message": "Customer added successfully"}), 200
        
        else:
            return jsonify({"error": "Invalid customer data"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/customers/<passportNumber>", methods=["DELETE"])
def remove_customer(passportNumber):
    global customer_data  

    customer_to_delete = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Find the index of the customer to remove by their passport number

    if customer_to_delete is not None:
        removed_customer = customer_data.pop(customer_to_delete)  # Removes the customer
        save_customers()
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
        save_customers()
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
        save_customers()
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
        save_customers()
        return jsonify({"message": "The customer's address of residence has been changed"}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route("/customers/<passportNumber>/email", methods=["PATCH"])
def change_customer_email(passportNumber):

    global customer_data  

    updated_email = request.json.get("email", "").strip()  # Get the new email from the request


    email_to_update = next((i for i, c in enumerate(customer_data) if c["passportNumber"] == passportNumber), None) # Finds the index of the customer to update from their passport number

    if email_to_update is not None:
        customer_data[email_to_update]["email"] = updated_email
        save_customers()
        return jsonify({"message": "The customer's email has been changed"}), 200
    
    else:
        return jsonify({"error": "Customer not found"}), 404

app.run()

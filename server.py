#flask --app server run

from flask import Flask
from flask import jsonify
from flask import json
from flask import request
import json


with open("vehicle.json") as vehicleJson:
   vehicle_data = json.load(vehicleJson)

with open ("customer.json") as customerJson:
    customer_data = json.load(customerJson)

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
    return "not found"

@app.route("/vehicles/make/<make>", methods=["GET"])
def get_make(make):
    matching_vehicles = [v for v in vehicle_data if v["make"] == make]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/year/<year>", methods=["GET"])
def get_year(year):
    matching_vehicles = [v for v in vehicle_data if v["year"] == year]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/vrm/<vrm>", methods=["GET"])
def get_vrm(vrm):
    matching_vehicles = [v for v in vehicle_data if v["vrm"] == vrm]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/category/<category>", methods=["GET"])
def get_category(category):
    matching_vehicles = [v for v in vehicle_data if v["category"] == category]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/numberSeats/<numberSeats>", methods=["GET"])
def get_numberSeats(numberSeats):
    matching_vehicles = [v for v in vehicle_data if v["numberSeats"] == numberSeats]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/dayRate/<dayRate>", methods=["GET"])
def get_dayRate(dayRate):
    matching_vehicles = [v for v in vehicle_data if v["dayRate"] == dayRate]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/branch/<branch>", methods=["GET"])
def get_branch(branch):
    matching_vehicles = [v for v in vehicle_data if v["branch"] == branch]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/status/<status>", methods=["GET"])
def get_status(status):
    matching_vehicles = [v for v in vehicle_data if v["status"] == status]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles/model/<model>", methods=["GET"])
def get_model(model):
    matching_vehicles = [v for v in vehicle_data if v["model"] == model]
    if matching_vehicles:
        return jsonify(matching_vehicles) 
    return "not found"

@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    try:
        new_vehicle = request.get_json()  
        if not new_vehicle:
            return jsonify({"error": "Invalid JSON data in request body"}), 400

        if "id" in new_vehicle and "make" in new_vehicle and "model" in new_vehicle and "colour" in new_vehicle and "vin" and "year" in new_vehicle and "vrm" in new_vehicle and "category" and "numberSeats" in new_vehicle and "dayRate" in new_vehicle and "status" in new_vehicle and "fuelEconomy" in new_vehicle and "branch" in new_vehicle:
            vehicle_data.append(new_vehicle)
            return jsonify({"message": "Vehicle added successfully"}), 200
        else:
            return jsonify({"error": "Invalid vehicle data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/vehicles/<vrm>", methods=["DELETE"])
def remove_vehicle(vrm):
    global vehicle_data  # Use the global variable
    # Find the index of the vehicle to remove
    index_to_remove = next((i for i, v in enumerate(vehicle_data) if v["vrm"] == vrm), None)

    if index_to_remove is not None:
        removed_vehicle = vehicle_data.pop(index_to_remove)  # Remove the vehicle
        return jsonify({"message": "Vehicle removed successfully", "removed_vehicle": removed_vehicle}), 200
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    
@app.route("/vehicles/<vrm>/status", methods=["PATCH"])
def change_vehicle_color(vrm):
    global vehicle_data  # Use the global variable
    updated_status = request.json.get("status", "").strip()  # Get the new color from the request JSON

    # Find the index of the vehicle to update
    index_to_update = next((i for i, v in enumerate(vehicle_data) if v["vrm"] == vrm), None)

    if index_to_update is not None:
        vehicle_data[index_to_update]["status"] = updated_status
        return jsonify({"message": "The vehicle has been rented"}), 200
    else:
        return jsonify({"error": "Vehicle not found"}), 404

app.run()
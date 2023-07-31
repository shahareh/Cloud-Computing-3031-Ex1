from flask import Flask, request, jsonify
import random
from datetime import datetime
import math


app = Flask(__name__)


# In-memory data store (for simplicity, we'll use a Python list)
parking_lots_db = {}
parking_plates_entered = []
parking_lots_in_use = []
generated_ticket_ids = []

def generate_unique_ticket_id():
    while True:
        # Generate a random 4-digit number between 1000 and 9999 (inclusive)
        number = random.randint(1000, 9999)
        
        # Check if the number is not in the list of existing numbers
        if number not in generated_ticket_ids:
            generated_ticket_ids.append(number)
            return number



def save_parking_details(plate, parking_lot,ticket_id):
    
    # Save the entry data in the data_store (you can add more logic here)
    parking_lots_db[ticket_id] = {
        "entry_time" : datetime.now(),
        "plate" : plate,
        "parking_lot" : parking_lot
    }

    parking_plates_entered.append(plate)
    parking_lots_in_use.append(parking_lot)


def get_parking_details_by_ticket_id(ticket_id):
    parking_details = parking_lots_db[ticket_id]
   
    parking_plates_entered.remove(parking_details['plate'])
    parking_lots_in_use.remove(parking_details['parking_lot'])
    del parking_lots_db[ticket_id]

    return parking_details
    

def calculate_parking_price(parking_total_minutes):
    parking_occurrences = math.ceil(parking_total_minutes / 15)
    price_per_hour = 10.0
    return parking_occurrences * (price_per_hour / 4)


@app.route('/entry', methods=['POST'])
def entry():
    plate = request.args.get('plate', '')
    parking_lot = request.args.get('parkingLot', '')
    
    if plate in parking_plates_entered:
        return "A Car with the same plate is already inside the parking area.", 422
    
    if parking_lot in parking_lots_in_use:
        return "This parking lot is already in use.", 422

    
    ticket_id = generate_unique_ticket_id()
    save_parking_details(plate, parking_lot,ticket_id)
    
    return jsonify({"ticketId": ticket_id}), 201



@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = request.args.get('ticketId', '')
    try:
        ticket_id = int(ticket_id)

    except ValueError:
        return "Invalid TicketId. Please provide a valid integer value.", 422

    if ticket_id not in parking_lots_db:
        return "TicketId is not exist.", 404
    
    parking_details = get_parking_details_by_ticket_id(ticket_id)
    parking_total_time = (datetime.now() - parking_details['entry_time']).total_seconds() / 60
    charge = calculate_parking_price(parking_total_time)

    return jsonify({
        'license_plate': parking_details['plate'],
        'parking_lot': parking_details['parking_lot'],
        'parking_time': parking_total_time,
        'charge': charge
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')

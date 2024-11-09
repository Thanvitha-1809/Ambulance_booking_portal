# app.py
import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# Pricing table for routes
pricing = {
    "Vikas Nagar-Anantapur": 250,
    "Vikas Nagar-Dharmavaram": 350,
    "Vikas Nagar-Hindupur": 450,
}

# Request handler for HTTP requests
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/book":
            query = parse_qs(parsed_path.query)
            pickup = query.get("pickup", [None])[0]
            drop = query.get("drop", [None])[0]
            condition = query.get("condition", [""])[0]

            route_key = f"{pickup}-{drop}"
            cost = pricing.get(route_key)

            if cost is None:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid route.")
                return

            conn = sqlite3.connect("ambulance.db")
            cursor = conn.cursor()
            
            # Retrieve driver details
            cursor.execute("SELECT * FROM drivers ORDER BY total_trips ASC LIMIT 1")
            driver = cursor.fetchone()
            if not driver:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"No drivers available.")
                conn.close()
                return

            driver_id, driver_name, driver_contact, total_trips, total_earnings = driver

            # Record patient booking
            cursor.execute('''
                INSERT INTO patients (name, pickup_location, drop_location, cost, driver_id, condition)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('Patient', pickup, drop, cost, driver_id, condition))

            # Update driver statistics
            cursor.execute('''
                UPDATE drivers
                SET total_trips = total_trips + 1, total_earnings = total_earnings + ?
                WHERE id = ?
            ''', (cost, driver_id))

            conn.commit()
            conn.close()

            response = {
                "cost": cost,
                "driver_name": driver_name,
                "driver_contact": driver_contact
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        elif parsed_path.path == "/suggestions":
            query = parse_qs(parsed_path.query)
            disease = query.get("disease", [""])[0]
            
            # Disease to hospital mapping
            disease_hospital_map = {
                "Cardiology": ["Heart Care Hospital", "Medline Cardiac Center", "City Heart Clinic"],
                "Orthopedics": ["Bone & Joint Hospital", "OrthoCare Clinic", "Orthopedic Specialty Hospital"],
                "Neurology": ["Brain Health Center", "Neurology Clinic", "City Neuro Hospital"],
                "Oncology": ["Cancer Treatment Center", "OncoCare Hospital", "Healing Hands Cancer Institute"],
                "Pediatrics": ["Child Care Hospital", "Happy Kids Clinic", "Pediatric Specialty Center"]
            }

            # Retrieve hospital suggestions based on disease
            suggestions = disease_hospital_map.get(disease, [])

            response = {
                "suggestions": suggestions
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        
        else:
            super().do_GET()

# Start the server
server = HTTPServer(('localhost', 8000), RequestHandler)
print("Server running on http://localhost:8000")
server.serve_forever()

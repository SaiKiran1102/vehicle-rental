from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.secret_key = "rental_secret"

# MongoDB Atlas Configuration
app.config["MONGO_URI"] = "mongodb+srv://saikiran:saikiran@cluster0.vvavmjo.mongodb.net/vehicledb"

mongo = PyMongo(app)

# Collections
users_collection = mongo.db.users
bookings_collection = mongo.db.bookings

# Vehicle data
vehicles = [
    {"id": "vehicle1", "name": "KTM Duke 200", "cost": 2500, "image": "200dukeimage.jpg"},
    {"id": "vehicle2", "name": "Honda Activa 6G", "cost": 1200, "image": "activa6gimage.png"},
    {"id": "vehicle3", "name": "TVS Apache RTR 160", "cost": 1600, "image": "apachertr160image.jpg"},
    {"id": "vehicle4", "name": "Royal Enfield Continental GT 650", "cost": 3000, "image": "continentalgt650image.png"},
    {"id": "vehicle5", "name": "Royal Enfield Classic", "cost": 2000, "image": "m_Buffalo_shop_(3).jpg"},
    {"id": "vehicle6", "name": "Toyota Innova", "cost": 2800, "image": "rbnjb0b_1622177.png"},
    {"id": "vehicle7", "name": "Yamaha R15 V4", "cost": 1700, "image": "r15v4image.png"},
    {"id": "vehicle8", "name": "Honda City", "cost": 2500, "image": "Honda_City_hatchback_exterior_1200x768.png"},
    {"id": "vehicle9", "name": "TVS Raider 125", "cost": 1500, "image": "raider125image.png"},
    {"id": "vehicle10", "name": "Honda SP 125", "cost": 1400, "image": "sp125image.jpg"},
    {"id": "vehicle11", "name": "TVS Ntorq 125", "cost": 1350, "image": "ntorq125image.png"},
    {"id": "vehicle12", "name": "Harley-Davidson X440", "cost": 4000, "image": "x440image.png"},
    {"id": "vehicle13", "name": "Royal Enfield Hunter 350", "cost": 2200, "image": "hunter350image.png"},
    {"id": "vehicle14", "name": "Hero Splendor Plus", "cost": 1000, "image": "splendorplusimage.png"},
    {"id": "vehicle15", "name": "Bajaj Pulsar RS 200", "cost": 1900, "image": "pulsarrs200image.png"},
    {"id": "vehicle16", "name": "Yamaha MT 15 V2", "cost": 1800, "image": "mt15v2image.png"},
    {"id": "vehicle17", "name": "Bajaj Pulsar NS200", "cost": 1850, "image": "pulsarns200image.png"},
    {"id": "vehicle18", "name": "Honda Shine", "cost": 1300, "image": "honda-cb-shine-sp-2018-athletic-blue-metallic-1522397192507.png"},
    {"id": "vehicle19", "name": "Royal Enfield Meteor 350", "cost": 2500, "image": "meteor350image.png"},
    {"id": "vehicle20", "name": "Hyundai Creta", "cost": 3500, "image": "cretacretarightfrontthreequarter.jpg"},
    {"id": "vehicle21", "name": "Maruti Suzuki Fronx", "cost": 3000, "image": "fronxfronxrightfrontthreequarter.jpg"},
    {"id": "vehicle22", "name": "Tata Curvv", "cost": 3200, "image": "curvvcurvvrightfrontthreequarter.jpg"},
    {"id": "vehicle23", "name": "Tata Nexon", "cost": 3100, "image": "nexonnexonrightfrontthreequarter.jpg"},
    {"id": "vehicle24", "name": "Mahindra BE 6", "cost": 3300, "image": "be6beerightfrontthreequarter.jpg"},
    {"id": "vehicle25", "name": "Mahindra Scorpio N", "cost": 3400, "image": "scorpionscorpionrightfrontthreequarter.jpg"},
    {"id": "vehicle26", "name": "Maruti Suzuki Brezza", "cost": 2900, "image": "brezzabrezzarightfrontthreequarter.jpg"},
    {"id": "vehicle27", "name": "Maruti Suzuki Dzire", "cost": 2700, "image": "dziredzirerightfrontthreequarter.jpg"},
    {"id": "vehicle28", "name": "Tata Punch", "cost": 2600, "image": "punchpunchrightfrontthreequarter.jpg"},
    {"id": "vehicle29", "name": "Toyota Urban Cruiser", "cost": 3000, "image": "urban-cruiser-hyryder-exterior-right-front-three-quarter-72.png"},
    {"id": "vehicle30", "name": "Maruti Suzuki Grand Vitara", "cost": 3100, "image": "grand-vitara-2009-2015.png"},
    {"id": "vehicle31", "name": "Maruti Suzuki Swift", "cost": 2600, "image": "swiftswiftrightfrontthreequarter.jpg"}
]

# ---------------------- Public Routes ----------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vehicles')
def vehicle_gallery():
    user_logged_in = 'user_id' in session
    return render_template('vehicles.html', user=user_logged_in, vehicles=vehicles)

# ---------------------- User Routes ----------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({"email": email, "password": password})

        if user:
            session['user_id'] = str(user['_id'])
            session['username'] = user['name']
            return redirect(url_for('home_loggedin'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = {
            "name": request.form['name'],
            "dob": request.form['dob'],
            "aadhar": request.form['aadhar'],
            "license": request.form['license'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "password": request.form['password']
        }
        users_collection.insert_one(new_user)
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/home')
def home_loggedin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index_user.html')

@app.route('/book/<vehicle_id>', methods=['GET', 'POST'])
def book(vehicle_id):
    if 'user_id' not in session:
        flash("Please login to book a vehicle.")
        return redirect(url_for('login'))

    selected_vehicle = next((v for v in vehicles if v["id"] == vehicle_id), None)
    if not selected_vehicle:
        flash("Vehicle not found.")
        return redirect(url_for('vehicle_gallery'))

    if request.method == 'POST':
        booking = {
            "user_id": session['user_id'],
            "user_name": session['username'],
            "vehicle": selected_vehicle["name"],
            "date": request.form['date'],
            "return_date": request.form['return_date'],
            "time": request.form['time'],
            "booked_at": datetime.now()
        }
        bookings_collection.insert_one(booking)
        flash("Booking confirmed!")
        return redirect(url_for('booking_history'))

    return render_template('booking.html', vehicle=selected_vehicle)

@app.route('/history')
def booking_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    bookings = bookings_collection.find({"user_id": user_id})
    return render_template('history.html', bookings=bookings)

# ---------------------- Admin Routes ----------------------

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']

        if login_id == 'SAI@2941' and password == '12345678':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid Admin ID or Password')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        flash("Admin access required.")
        return redirect(url_for('admin_login'))

    bookings = bookings_collection.find()
    return render_template('admin_dashboard.html', bookings=bookings)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash("Admin logged out.")
    return redirect(url_for('admin_login'))

# ---------------------- Logout ----------------------

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('index'))

# ---------------------- App Runner ----------------------

if __name__ == '__main__':
    app.run(debug=True)
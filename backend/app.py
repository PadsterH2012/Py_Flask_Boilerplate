from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydatabase'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
    username = data['username']
    password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful!'})
    
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully!'})

@app.route('/')
def index():
    return render_template('index.html')  # Ensure this is rendering the correct template

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')  # Ensure this template exists in the templates directory

def connect_to_database(retries=5, delay=5):
    try:
        for attempt in range(retries):
            try:
                with app.app_context():
                db.create_all()
            print("Successfully connected to the database!")
            return
        except OperationalError as e:
            if attempt < retries - 1:
                print(f"Database connection attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Failed to connect to the database after multiple attempts.")
                raise e

if __name__ == '__main__':
    connect_to_database()
    app.run(host='0.0.0.0', port=5000)

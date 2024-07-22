from flask import Flask, request, jsonify, session, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import time
from sqlalchemy.exc import OperationalError
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'), static_folder=os.path.abspath('static'))
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydatabase'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username, email, or password'}), 400
    
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful!', 'redirect': url_for('dashboard')})
    
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

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    return render_template('dashboard.html')

@app.route('/user_settings')
def user_settings():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    user = User.query.get(session['user_id'])
    return render_template('user_settings.html', username=user.username, email=user.email)

@app.route('/app_settings')
def app_settings():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    return render_template('app_settings.html')

def connect_to_database(retries=5, delay=5):
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

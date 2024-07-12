from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuring a database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JWT
app.config['JWT_SECRET_KEY'] = '12345'  #The key 12345 can change as per you one wants.

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model for holding details (email, phone_no and password).
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    phone_no = db.Column(db.Integer, unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)


# Initialize database even before first html page is rendered.
with app.app_context():
    db.create_all()


# 1st page to Login page
@app.route('/', methods = ['GET'])
def login_page():
    return render_template('login.html')


# Login endpoint for an existing user.
@app.route('/login_api', methods = ['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']

    #Check if the entered Email is found in the db (User table) or not.
    #Encrypting the password so that, even when looking at db, password is encoded.
    user = User.query.filter_by(email = email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity = user.id)
        return jsonify(access_token = access_token)

    #When user does not exist.
    return render_template('login.html', Message = "Invalid credentials")


# Registration endpoint for a new user.
@app.route('/register_api', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    email = request.form["email"]
    phone_no = request.form['phone_no']
    password = request.form["password"]
    #Using hash function to hide the password in sqlite db.
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    #Checking if Email or Phone_no , already exist.
    user = User.query.filter_by(email = email).first()
    if user:
        return render_template("register.html", Message = "Email is already registered!")
    user_1 = User.query.filter_by(phone_no = phone_no).first()
    if user_1:
        return render_template("register.html", Message = "Phone no. is already registered!")

    #If new entries then register the user.
    new_user = User(email = email, phone_no = phone_no, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return render_template("register.html", Message = "Successfully registered")


# Protected route, which will be access only when user is logged in or authorized.
@app.route('/protected_api', methods = ['GET'])
@jwt_required()
def protected():
    #You code for admin control goes here.
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user), 200

#Deleting and then creating the table.
#Is used only for debigging purpose.
@app.route('/delete_database', methods = ['GET'])
def delete_database():
    db.drop_all()
    db.create_all()
    return jsonify(message = "Database deleted successfully"), 200

#To check the registered Users.
@app.route('/show_all_data', methods = ['GET'])
def show_all_data():
    users = User.query.all()
    users_list = [{'id': user.id, 'email': user.email, 'phone_no': user.phone_no, 'password': user.password,  } for user in users]
    return jsonify(users = users_list), 200


if __name__ == '__main__':
    app.run(debug = True)

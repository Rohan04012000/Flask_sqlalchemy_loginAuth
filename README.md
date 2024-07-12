This project was developed using Pychar(Virtual environment), tested using Postman.

# Method 1 - How to use the project.
1. Create a virtual environment, load the "login_Auth.py" file.
2. Then, start the server by typing the following command in the terminal:
   "python login_Auth.py
3. This will start the server and provide a URL. Use that URL to access all the endpoints through Chrome or similar services.

### This project covers the login authentication and registration process, handling all edge cases and using an encoding method to hide the user's password. <br> 
# Key features include:

## User Authentication:

1. Login endpoint for existing users.
2. Generates JWT access tokens upon successful login.
3. Protected routes accessible only with valid JWT tokens.

## User Registration:

1. Registration endpoint for new users.
2. Checks for unique constraints on both email and phone number.
3. Uses bcrypt to hash and securely store user passwords.

## Database Operations:

1. Initializes the database before rendering the first HTML page.
2. Provides an endpoint to delete and recreate the database.

## Endpoints:

1. Login Page (/): <br>
Renders the login HTML page.

2. Login API (/login_api):<br>
Handles GET and POST requests.<br>
Checks user credentials and returns an access token on success.<br>

3. Registration API (/register_api):<br>
Handles GET and POST requests.<br>
Ensures email and phone number are unique before registering a new user.<br>

4. Protected API (/protected_api):<br>
Requires a valid JWT token.<br>
Returns the identity of the logged-in user.<br>

5. Delete Database (/delete_database):<br>
Drops and recreates the database.

6. Show All Data (/show_all_data):<br>
Retrieves and displays all data from the User table.<br>

7. Security:<br>
Utilizes JWT for secure authentication.<br>
Employs bcrypt for password hashing.<br>

8. Edge Case Handling:<br>
Proper validation and feedback for duplicate email or phone number during registration.<br>
Appropriate error messages for invalid login credentials.<br>

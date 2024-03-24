from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'kd'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'admin123'
# app.config['MYSQL_DB'] = 'expense_tracker'
#
# mysql = MySQL(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'home'
#
# class User(UserMixin):
#     pass
#
# @login_manager.user_loader
# def load_user(user_id):
#     # Connect to MySQL database
#     cur = mysql.connection.cursor()
#
#     # Execute a query to fetch user information based on user_id
#     cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#     user_data = cur.fetchone()
#
#     # Close the cursor
#     cur.close()
#
#     if user_data:
#         # Create a User object using the fetched user data
#         user = User()
#         user.id = user_data['id']
#         # Assign other attributes of the user as needed
#         return user
#     else:
#         return None


@app.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    # Fetch expenses for current user from database
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM expenses WHERE user_id = %s", (current_user.id,))
    # expenses = cur.fetchall()
    # cur.close()
    expenses = ''
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        expenses = f"date: {date} des: {description} amt: {amount}"
    return render_template('home.html', exp=expenses)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registered = ''
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c_password = request.form['c_password']
        if c_password != password:
            error = 'password did not match'
            c_password = ''
        registered = f"username : {username} password : {c_password}"
    return render_template('register.html', registered=registered, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logged = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logged = f"username : {username} password : {password}"
    return render_template('login.html', logged=logged)


if __name__ == '__main__':
    app.run(debug=False)


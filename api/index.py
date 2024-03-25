from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kd'
app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6694060'
app.config['MYSQL_PASSWORD'] = 'nwgRj3ghmR'
app.config['MYSQL_DB'] = 'sql6694060'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.static_folder = 'static'


bcrypt = Bcrypt(app)
#
mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        user = User(user_id)
        user.id = user_data['id']
        return user
    else:
        return None


def create_user_table():
    cur = mysql.connection.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTO_INCREMENT, 
        username VARCHAR(25),
        password VARCHAR(255))''')
    cur.close()


def create_expenses_table():
    cur = mysql.connection.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        user_id INTEGER,
        date DATE,
        description VARCHAR(255),
        amount FLOAT,
        FOREIGN KEY (user_id) REFERENCES users(id))''')
    cur.close()


def delete_tables():
    cur = mysql.connection.cursor()
    cur.execute('''DROP TABLE expenses''')
    cur.execute('''DROP TABLE users''')
    cur.close()

def register_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cur = mysql.connection.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cur.execute(query, (username, hashed_password))
    mysql.connection.commit()
    cur.close()


def verify_login(username, password):
    with app.app_context():  # Creating application context
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user['password'], password):
            return User(user['id'])
        return None


def fetch_expenses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id = %s", (current_user.id,))
    expenses = cur.fetchall()
    cur.close()
    return expenses


def add_expenses(date, user, description, amount):
    cur = mysql.connection.cursor()
    query = "INSERT INTO expenses (date,user_id,description,amount) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (date, user.id, description, amount))
    mysql.connection.commit()
    cur.close()


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    expenses = fetch_expenses()
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        add_expenses(date, current_user, description, amount)
        return redirect(url_for('home'))
    return render_template('home.html', expenses=expenses)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['c_password']
        if password == confirm_password:
            register_user(username, password)
            message = 'Registered successfully!'
        else:
            error = 'Passwords do not match'
    return render_template('register.html', error=error, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    create_user_table()
    create_expenses_table()
    message = ''
    # delete_tables()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_login(username, password)
        if user:
            login_user(user)
            return redirect(url_for('home'))  # Redirect to home page upon successful login
        else:
            message = 'Invalid username or password'  # Display error message for invalid login
    return render_template('login.html', message=message)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # return redirect(url_for('login'))
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=False)


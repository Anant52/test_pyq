from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Update with your MySQL root password
    'database': 'pyq_portal'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Email already exists. Please log in."

        # Insert user into the database
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))

        return "Invalid email or password."

    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    user_name = session['user_name']

    # Example data for the dashboard
    papers = [
        {'subject': 'BBA', 'year': 2023, 'title': 'BBA Paper 2023'},
        {'subject': 'BCA', 'year': 2022, 'title': 'BCA Paper 2022'},
        {'subject': 'BCom', 'year': 2021, 'title': 'BCom Paper 2021'}
    ]

    return render_template('dashboard.html', user_name=user_name, papers=papers)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)

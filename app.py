from flask import Flask, render_template, request, session
import time, logging
from app2 import app2

booking_details_list = []
active_users = {}
"""log = logging.getLogger('werkzeug')    # we can hide logging info 
log.setLevel(logging.ERROR)"""

app = Flask(__name__)

app.register_blueprint(app2, url_prefix='/app2')

@app.route('/')
def index():
    # To count current number of users are logged in 
    session['user_id'] = str(time.time())  # Unique session ID based on timestamp
    active_users[session['user_id']] = time.time()  # Track session start time
    active_users_count()
    return render_template('index.html', title='Coffee Shop')

def active_users_count():
    # Cleanup sessions that are older than a set threshold (e.g., 5 minutes)
    threshold = time.time() - 300  # 5 minutes threshold
    active_users_cleaned = {user_id: start_time for user_id, start_time in active_users.items() if start_time > threshold}

    # Update the active users
    active_users.clear()
    active_users.update(active_users_cleaned)

    print(len(active_users))


@app.route('/book_a_table', methods=['POST'])
def book_a_table():
    # Accessing data from index.html of appointment table
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    print(f_name," ", l_name," ", email," ", phone," ", message)

    booking_details = {
        'f_name': f_name,
        'l_name': l_name,
        'email': email,
        'phone': phone,
        'message': message
    }

    booking_details_list.append(booking_details)

    return render_template('index.html', title='Coffee Shop')

@app.route('/list_orders')
def list_orders():
    return render_template('list_orders.html', booking_details_list=booking_details_list)

if __name__ == "__main__":
    app.secret_key = 'manoj_rajgopal'
    app.logger.setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=5000, debug=True)

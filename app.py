from flask import Flask, render_template, request, redirect, url_for, session
from routes.patient_routes import patient_bp
from routes.admission_routes import admission_bp
from jinja2 import FileSystemLoader
from routes.doctor_routes import doctor_bp
from routes.appointment_routes import appointment_bp


app = Flask(__name__)
#below is force to block caching
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True
app.jinja_loader = FileSystemLoader('templates')

app.secret_key = 'Monia47'  # Needed for session management

app.register_blueprint(patient_bp, url_prefix='/patients')
app.register_blueprint(admission_bp, url_prefix='/admissions')
app.register_blueprint(doctor_bp, url_prefix='/doctors')
app.register_blueprint(appointment_bp, url_prefix='/appointments')

# Hardcoded credentials (for now)
USERS = {
    'admin': '123'
}

@app.route('/')
def home():
    is_logged_in = 'user' in session
    return render_template('index.html', is_logged_in=is_logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

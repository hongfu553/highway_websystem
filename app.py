from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
from mqtt_test_tools.mqtt_check import check_mqtt_status
from datetime import datetime,timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.atsxuiflbxzohuutmdnh:*$c?MT+?7vqrF7a@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mqtt_broker = "amd2.oracle.kenchou2006.eu.org"
mqtt_port = 1883
mqtt_topic = "tofu/road"

client = mqtt.Client('web')
client.connect(mqtt_broker, mqtt_port)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

utc= timedelta(hours=8)
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + utc)
    message = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f"<Log(id={self.id}, timestamp='{self.timestamp}', message='{self.message}')>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    try:
        mqtt_status = check_mqtt_status(mqtt_broker, mqtt_port)
        if mqtt_status:
            show_mqtt_status="Connect"
        else:
            show_mqtt_status = "Not Connect"
    except Exception as e:
        show_mqtt_status = "Not Connect"
    return render_template('index.html', mqtt_status=show_mqtt_status)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        mv = request.form['mv']
        print(mv)
        client.publish(mqtt_topic,mv)
        log_entry = Log(message=mv)
        db.session.add(log_entry)
        db.session.commit()
        logs = Log.query.all()
    else:
        logs = Log.query.all()
    return render_template('control.html',logs=logs)

@app.route('/clear_logs',methods=['POST'])
def clear_logs():
    if request.method == 'POST':
        Log.query.delete()
        db.session.commit()
        return redirect(url_for('control'))

@app.before_request
def before_request():
    if not request.path.startswith('/login') and not request.path.startswith('/static'):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



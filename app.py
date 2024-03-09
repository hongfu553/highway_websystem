from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


mqtt_broker_address = "broker.hivemq.com"
mqtt_broker_port = 1883
mqtt_topic = "hongfu553/road"


mqtt_client = mqtt.Client()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

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
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    mqtt_connect = True
    return render_template('index.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/control')
def control():
    return render_template('control.html')


@app.before_request
def before_request():
    if not request.path.startswith('/login') and not request.path.startswith('/static'):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))


def mqtt_connect():
    mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    mqtt_client.loop_start()

def on_message(client, userdata, message):
    print("Received message:", message.payload.decode())


mqtt_client.on_message = on_message

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        mqtt_connect()   
        mqtt_client.subscribe(mqtt_topic)
    app.run(debug=True, port=8000)

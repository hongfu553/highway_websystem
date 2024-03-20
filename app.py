from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
# Update the database URI to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.atsxuiflbxzohuutmdnh:*$c?MT+?7vqrF7a@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mqtt_broker = "hongfu553.myds.me"
mqtt_port = 1883
mqtt_topic = "tofu/road"

client= mqtt.Client()
client.connect(mqtt_broker,mqtt_port)

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
        ('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    result = client.publish(mqtt_topic, message)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Message published successfully")
    else:
        print("Failed to publish message")

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)

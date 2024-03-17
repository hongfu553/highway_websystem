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
mqtt_message = None

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
        # 添加登录失败的提示消息
        flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    global mqtt_message
    mqtt_connect()  # 调用 mqtt_connect 函数以建立 MQTT 连接
    return render_template('index.html', mqtt_message=mqtt_message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/control')
def control():
    return render_template('control.html')

def handle_mqtt_message(client, userdata, message):
    global mqtt_message
    payload = message.payload.decode('utf-8')
    print(f"Received message: {payload}")
    mqtt_message = payload

mqtt_client.on_message = handle_mqtt_message

def mqtt_connect():
    mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    mqtt_client.loop_start()  # 启动 MQTT 客户端循环
    print('Connected to MQTT broker')
    mqtt_client.subscribe(mqtt_topic)

@app.before_request
def before_request():
    if not request.path.startswith('/login') and not request.path.startswith('/static'):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False) 

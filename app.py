from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.atsxuiflbxzohuutmdnh:*$c?MT+?7vqrF7a@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

mqtt_broker = "arm2.oracle.kenchou2006.eu.org"
mqtt_port = 1883
mqtt_topic = "tofu/road"
status_topic = "tofu/status" # Status topic to check connection
mqtt_username = 'hongfu553'
mqtt_password = 'F132369445'

client = mqtt.Client('web')
client.username_pw_set(mqtt_username, mqtt_password)
#client.tls_set(cert_reqs=ssl.CERT_NONE)
client.connect(mqtt_broker, mqtt_port)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

utc = timedelta(hours=8)
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
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('帳號密碼錯誤!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']  
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('此帳號名稱已被使用', '危險')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))  # 如果用戶已登入，則導向主頁面
    else:
        return redirect(url_for('login'))  # 如果用戶尚未登入，則導向登入頁面

@app.route('/main')
@login_required
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/control', methods=['GET', 'POST'])
@login_required
def control():
    if request.method == 'POST':
        mv = request.form['mv']
        print(mv)
        # Check ESP32 connection status
        if not check_mqtt_status():
            flash('ESP32 not connected to MQTT broker!', 'danger')
            return redirect(url_for('control'))
        
        client.publish(mqtt_topic, mv)
        log_entry = Log(message=mv)
        db.session.add(log_entry)
        db.session.commit()
        logs = Log.query.all()
    else:
        logs = Log.query.all()
    return render_template('control.html', logs=logs)

def check_mqtt_status():
    status = False

    def on_message(client, userdata, msg):
        nonlocal status
        if msg.topic == status_topic and msg.payload.decode() == "connected":
            status = True

    client.subscribe(status_topic)
    client.on_message = on_message
    client.loop_start()
    client.publish(status_topic, "check")

    # Wait for a short period to receive the status message
    time.sleep(2)
    client.loop_stop()

    return status

@app.route('/clear_logs', methods=['POST'])
@login_required
def clear_logs():
    if request.method == 'POST':
        Log.query.delete()
        db.session.commit()
        return redirect(url_for('control'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

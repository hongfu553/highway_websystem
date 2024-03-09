from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 資料庫檔案位置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

# 建立 Flask-Login 登入管理器
login_manager = LoginManager()
login_manager.init_app(app)

# MQTT 連接參數
mqtt_broker_address = "broker.hivemq.com"
mqtt_broker_port = 1883
mqtt_topic = "hongfu553/road"

# 建立 MQTT 客戶端
mqtt_client = mqtt.Client()

# 假設的使用者資料表模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 登入頁面
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

# 登出頁面
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 頁面
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

# 確認登入
@app.before_request
def before_request():
    if not request.path.startswith('/login') and not request.path.startswith('/static'):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

# MQTT 連接設定
def mqtt_connect():
    mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    mqtt_client.loop_start()

# 當接收到 MQTT 訊息時的處理函數
def on_message(client, userdata, message):
    # 在這裡處理接收到的 MQTT 訊息
    print("Received message:", message.payload.decode())

# 設定 MQTT 客戶端的訊息處理函數
mqtt_client.on_message = on_message

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 在應用程式上下文中創建資料庫表格
        mqtt_connect()   # 連接到 MQTT broker
        mqtt_client.subscribe(mqtt_topic)  # 訂閱 MQTT 主題
    app.run(debug=True, port=8000)

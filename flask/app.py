from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, Users, Log, add_log, init_db
from admin import init_admin
from dotenv import load_dotenv
import os
import mqtt_process

# Load environment variables
load_dotenv()
sec_key = os.getenv('SECRET_KEY')
db_uri = os.getenv('database')

app = Flask(__name__)
app.config['SECRET_KEY'] = sec_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Initialize extensions
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
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
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('密碼不一致', 'danger')
            return redirect(url_for('register'))
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('此帳號名稱已被使用', 'danger')
        else:
            try:
                new_user = Users(username=username)
                new_user.password = password  # 這將會雜湊密碼
                db.session.add(new_user)
                db.session.commit()
                flash('你的帳號已建立！現在可以登入。', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'註冊時出現錯誤: {str(e)}', 'danger')
                app.logger.error(f'註冊時出現錯誤: {str(e)}')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))

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
        mqtt_process.publish_message('tofu/road', mv)
        add_log(mv)
    logs = Log.query.all()
    return render_template('control.html', logs=logs)

@app.route('/clear_logs', methods=['POST'])
@login_required
def clear_logs():
    Log.query.delete()
    db.session.commit()
    return redirect(url_for('control'))

init_admin(app,db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
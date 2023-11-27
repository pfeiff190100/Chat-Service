from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db.model import db
from db.handler import add_user, get_user, add_message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'verysecretyesyes'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return load_user(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    add_user(data['username'], data['password'])
    return jsonify({'message': 'Registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user(data['username'])
    if user and user.password == data['password']:
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'message': 'Invalid credentials'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    recipient = get_user(data['recipient'])
    if recipient:
        add_message(current_user.id, recipient.id, data['message'])
        return jsonify({'message': 'Message sent'})
    return jsonify({'message': 'Recipient not found'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=25565,debug=True)
import jwt
from flask import Flask, jsonify, make_response, request, session, flash
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps

from db.handler import add_message, add_user, get_all_messages, get_user
from db.handler import load_user as get_user_by_id
from db.model import db
from config import DefaultConfig

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.secret_key = config_object.SECRET_KEY

    active_tokens = {}

    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = get_user_by_id(int(user_id))
        return user if user else None

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            user_id = active_tokens.get(token)
            if not user_id:
                return jsonify({'message': 'Token is invalid!'}), 401
            return f(user_id, *args, **kwargs)
        return decorated


    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            flash('Missing username or password')
            return jsonify({'message': 'Bad Request', 'error': 'Missing username or password'}), 400
        user = get_user(data['username'])
        if user and user.password == data['password']:
            remember = data.get('remember', False)
            login_user(user, remember=remember)
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'])
            active_tokens[token] = user.id
            return jsonify({'message': 'Logged in successfully', 'token': token}), 200
        flash('Invalid credentials')
        return jsonify({'message': 'Unauthorized', 'error': 'Invalid credentials'}), 401

    @app.route('/logout')
    @login_required
    @token_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/checkuser', methods=['POST'])
    @token_required
    def checkuser(user_id):
        data = request.get_json()
        if 'username' not in data:
            return jsonify({'message': 'Bad Request', 'error': 'Missing username'}), 400
        user = get_user(data['username'])
        if user is not []:
            return jsonify({'message': 'True'}), 200
        return jsonify({'message': 'False',}), 200

    @app.route('/send_message', methods=['POST'])
    @token_required
    def send_message(user_id):
        data = request.get_json()
        if 'recipient' not in data or 'body' not in data:
            return jsonify({'message': 'Bad Request', 'error': 'Missing recipient or body'}), 400
        if  len(data['body']) > 500 or len(data['body']) == 0 or data['body'] == "":
            return jsonify({'message': 'Bad Request', 'error': 'Invalid body'}), 400

        recipient = get_user(data['recipient'])
        if recipient:
            add_message(user_id, recipient.id, data['body'])
            return jsonify({'message': 'Message sent'}), 201
        return jsonify({'message': 'Not Found', 'error': 'Recipient not found'}), 404

    @app.route('/get_messages', methods=['POST'])
    @token_required
    def get_messages(user_id):
        data = request.get_json()
        if 'recipient' not in data:
            return jsonify({'message': 'Bad Request', 'error': 'Missing recipient'}), 400
        recipient = get_user(data['recipient'])
        if recipient:
            messages = get_all_messages(user_id, recipient.id)
            messages_data = [{'sender': get_user_by_id(msg.sender_id).username, 
                            'recipient': get_user_by_id(msg.recipient_id).username, 'body': msg.body} 
                            for msg in messages]
            return jsonify({'messages': messages_data, 'message': 'Messages retrieved'}), 200
        return jsonify({'message': 'Not Found', 'error': 'Recipient not found'}), 404
    return app

if __name__ == '__main__':
    app = create_app(DefaultConfig)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=25565, debug=True)

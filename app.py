from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db.model import db
from db.handler import add_user, get_user, add_message, get_all_messages, load_user as get_user_by_id

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

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

    @app.route('/get_messages', methods=['POST'])
    @login_required
    def get_messages():
        data = request.get_json()
        recipient = get_user(data['recipient'])
        if recipient:
            messages = get_all_messages(current_user.id, recipient.id)
            messages_data = [{'sender': get_user_by_id(msg.sender_id).username, 
                            'recipient': get_user_by_id(msg.recipient_id).username, 'body': msg.body} 
                            for msg in messages]
            return jsonify({'messages': messages_data, 'message': 'Messages retrieved'})
        return jsonify({'message': 'Recipient not found'})
    return app

if __name__ == '__main__':
    app = create_app('config.DefaultConfig')
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=25565, debug=True)
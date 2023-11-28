from db.model import db, User, Message

def add_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

def get_user(username):
    return User.query.filter_by(username=username).first()

def load_user(user_id):
    return User.query.get(int(user_id))

def add_message(sender_id, recipient_id, body):
    msg = Message(sender_id=sender_id, recipient_id=recipient_id, body=body)
    db.session.add(msg)
    db.session.commit()

def get_all_messages(user1_id, user2_id):
    return Message.query.filter(
        (Message.sender_id == user1_id) & (Message.recipient_id == user2_id) |
        (Message.sender_id == user2_id) & (Message.recipient_id == user1_id)
    ).order_by(Message.timestamp).all()


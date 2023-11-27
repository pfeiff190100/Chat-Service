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

def get_all_messages(sender_id, recipient_id):
    return Message.query.filter_by(sender_id=sender_id, recipient_id=recipient_id).all()

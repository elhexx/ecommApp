from main import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    reg_status = db.Column(db.Integer, default = 0)

    def __init__(self, fname, lname, username, email, password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))

    def __init__(self, fname, lname, username, email, password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.password = password

def createUser(fname, lname, username, email, password):
    db.create_all()
    user = Users(fname, lname, username, email, password)
    db.session.add(user)
    db.session.commit()

def getUsers():
    users = Users.query.all()
    user_list = [user.username for user in users]
    return user_list

def getUser(username):
    user = Users.query.filter_by(username = username).first()
    return user

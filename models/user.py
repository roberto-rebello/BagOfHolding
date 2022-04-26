from models import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _username = db.Column(db.String(50), nullable = False)
    _password = db.Column(db.String(128), nullable = False)

    def __init__(self, username, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self._username = username
        self._password = password

    def __str__(self):
        return "Username: {}\n\tID: {}\n".format(self._username, str(self._id))

    def __repr__(self):
        return "<User {}>".format(self._id)

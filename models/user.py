from models import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _username = db.Column(db.String(50), nullable = False)
    _password = db.Column(db.String(128), nullable = False)
    _isAdmin  = db.Column(db.String(3), default = "No")

    def __init__(self, username, password, is_admin, **kwargs):
        super(User, self).__init__(**kwargs)
        self._username = username
        self._password = password
        self._isAdmin = is_admin

    def __str__(self):
        return "ID: {}\n\tUsername: {}\n\tAdmin: {}\n".format( str(self._id), self._username, self._isAdmin)

    def __repr__(self):
        return "<User {}>".format(self._id)

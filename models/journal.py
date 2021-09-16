from models import db
from datetime import datetime

class Journal(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _author = db.Column(db.String(100), nullable = False)
    _title = db.Column(db.String(500), default = "")
    _is_private = db.Column(db.Boolean, default=False)
    _user = db.Column(db.String(100), default = "")
    _creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, author, title="", is_private=False, user="", **kwargs):
        super(Journal, self).__init__(**kwargs)
        self._author = author
        self._title = title
        self._is_private = is_private
        self._user = user

    def __str__(self):
        return "ID: {}\n\tTitle: {}\n\tAuthor: {}\n\tCreation: {}\n\tPrivate: {}\n".format(str(self._id), self._title,
            self._author, str(self._creation_date), str(self._is_private))

    def __repr__(self):
        return "<Journal {}>".format(self._id)

class Entry(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _author = db.Column(db.String(100), nullable = False)
    _title = db.Column(db.String(500), default = "")
    _body = db.Column(db.Text, default="")
    _game_date = db.Column(db.String(50), default="")
    _location = db.Column(db.String(50), default="")
    _journal = db.relationship("Journal", backref=db.backref("entries", lazy=True))
    _journal_id = db.Column(db.Integer, db.ForeignKey("journal._id"), nullable=False)
    _creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _edit_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, journal, author, title="", body="", game_date="", location="", **kwargs):
        super(Entry, self).__init__(**kwargs)
        self._author = author
        self._title = title
        self._body = body
        self._game_date = game_date
        self._location = location
        self._journal = journal

    def __str__(self):
        return "ID: {}\n\tTitle: {}\n\tAuthor: {}\n\tCreation: {}\n\tBody: {}\n\tDate: {}\n\tLocation: {}\n".format(
            str(self._id), self._title, self._author, str(self._creation_date), self._body, self._game_date,
            self._location)

    def __repr__(self):
        return "<Entry {}, Journal {}>".format(self._id, self._journal_id)

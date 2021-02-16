from models import db

class Coin(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _name = db.Column(db.String(50), nullable = False)
    _value = db.Column(db.Integer, nullable = False, default = 1)
    _quantity = db.Column(db.Integer, nullable = False, default = 0)

    def __init__(self, name, value, quantity, **kwargs):
        super(Coin, self).__init__(**kwargs)
        self._name = name
        self._value = value
        self._quantity = quantity

    def __str__(self):
        return "Item: {}\n\tID: {}\n\tUnit value: {}\n\tQuantity: {}\n".format(self._name, str(self._id), str(self._value),
            str(self._quantity))

    def __repr__(self):
        return "<Coin {}>".format(self._id)

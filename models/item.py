from models import db

class Item(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _name = db.Column(db.String(200), nullable = False)
    _description = db.Column(db.String(500), default = "")
    _location = db.Column(db.String(500), default = "")
    _price = db.Column(db.Float, default = 0)
    _weight = db.Column(db.Float, default = 0)
    _quantity = db.Column(db.Integer, default = 1)
    _type = db.Column(db.String(50), default = "")
    _isMagic = db.Column(db.String(3), default = "No")
    _href = db.Column(db.String(100), default = "")

    def __init__(self, name, description, location, price, weight, quantity, type, isMagic, href, **kwargs):
        super(Item, self).__init__(**kwargs)
        self._name = name
        self._description = description
        self._location = location
        self._price = price
        self._weight = weight
        self._quantity = quantity
        self._type = type
        self._isMagic = isMagic
        self._href = href

    def __str__(self):
        return "Item: {}\n\tID: {}\n\tDescription: {}\n\tLocation: {}\n\tUnit price: {}\n\tUnit weight:: {}\n\tQuantity:"\
            " {}\n\tType: {}\n\tMagical: {}\n\thref: {}\n".format(self._name, str(self._id), self._description,
            self._location, str(self._price), str(self._weight), str(self._quantity), self._type, self._isMagic, self._href)

    def __repr__(self):
        return "<Item {}>".format(self._id)

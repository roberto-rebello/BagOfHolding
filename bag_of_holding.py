import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///bag.db'

db = SQLAlchemy(app)

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

@app.route("/", methods = ["POST", "GET"])
def index():
    if flask.request.method == "POST":
        new_item = Item(flask.request.form["name"],
                        flask.request.form["description"],
                        flask.request.form["location"],
                        flask.request.form["price"],
                        flask.request.form["weight"],
                        flask.request.form["quantity"],
                        flask.request.form["type"],
                        flask.request.form["isMagic"],
                        flask.request.form["href"])

        try:
            db.session.add(new_item)
            db.session.commit()
            return flask.redirect("/")

        except Exception as e:
            raise
    else:
        items = Item.query.order_by(Item._name).all()
        items_value = _getValue(items)
        items_weight = _getWeight(items)
        return flask.render_template("index.html", items=items, items_value=items_value, items_weight=items_weight)

@app.route("/create")
def create_item():
    return flask.render_template("create.html")

@app.route("/delete/<int:id>")
def delete_item(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return flask.redirect("/")

    except Exception as e:
        raise

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_item(id):
    item = Item.query.get_or_404(id)

    if flask.request.method == "POST":
        item._name = flask.request.form["name"]
        item._description = flask.request.form["description"]
        item._location = flask.request.form["location"]
        item._price = flask.request.form["price"]
        item._weight = flask.request.form["weight"]
        item._quantity = flask.request.form["quantity"]
        item._type = flask.request.form["type"]
        item._isMagic = flask.request.form["isMagic"]
        item._href = flask.request.form["href"]

        try:
            db.session.commit()
            return flask.redirect("/")
        except Exception as e:
            raise

    else:
        return flask.render_template("update.html", item=item)

@app.route("/copy/<int:id>")
def copy_item(id):
    item = Item.query.get_or_404(id)
    new_item = Item(item._name,
                    item._description,
                    item._location,
                    item._price,
                    item._weight,
                    item._quantity,
                    item._type,
                    item._isMagic,
                    item._href)

    try:
        db.session.add(new_item)
        db.session.commit()
        return flask.redirect("/")

    except Exception as e:
        raise


@app.route("/add/<int:id>")
def add_item(id):
    item = Item.query.get_or_404(id)

    item._quantity += 1

    try:
        db.session.commit()
        return flask.redirect("/")
    except Exception as e:
        raise

@app.route("/subtract/<int:id>")
def subtract(id):
    item = Item.query.get_or_404(id)

    item._quantity -= 1

    try:
        db.session.commit()
        return flask.redirect("/")
    except Exception as e:
        raise

def _getValue(items):
    total_value = 0.0
    for item in items:
        total_value += (item._price * item._quantity)

    return round(total_value, 1)

def _getWeight(items):
    total_weight = 0.0
    for item in items:
        total_weight += (item._weight * item._quantity)

    return round(total_weight, 1)

if __name__ == '__main__':
    app.run(debug=True)

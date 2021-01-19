import flask
import flask_sqlalchemy as sql

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///bag.db'

db = sql.SQLAlchemy(app)

class Item(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    _name = db.Column(db.String(200), nullable = False)
    _description = db.Column(db.String(500), default = "")
    _price = db.Column(db.Integer, default = 0)
    _weigth = db.Column(db.Integer, default = 0)
    _quantity = db.Column(db.Integer, default = 1)
    _type = db.Column(db.String(50), default = "")
    _isMagic = db.Column(db.String(3), default = "No")
    _href = db.Column(db.String(100), default = "")

    def __init__(self, name, description, price, weigth, quantity, type, isMagic, href):
        self._name = name
        self._description = description
        self._price = price
        self._weigth = weigth
        self._quantity = quantity
        self._type = type
        self._isMagic = isMagic
        self._href = href

    def __string__(self):
        return "Item: {}\n\tID: {}\n\tDescription: {}\n\tUnit price: {}\n\tUnit weight:: {}\n\tQuantity: {}\n\tType: "\
            "{}\n\tMagical: {}\n\thref: {}\n\t".format(self._name, str(self._id), self._description, str(self._price),
            str(self._weigth), str(self._quantity), self._type, self._isMagic, self._href)

    def __repr__(self):
        return "<Task {}>".format(self._id)

@app.route("/", methods = ["POST", "GET"])
def index():
    if flask.request.method == "POST":
        new_item = Item(flask.request.form["name"],
                        flask.request.form["description"],
                        flask.request.form["price"],
                        flask.request.form["weigth"],
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
        return flask.render_template("index.html", items=items)

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
        item._price = flask.request.form["price"]
        item._weigth = flask.request.form["weigth"]
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
                    item._price,
                    item._weigth,
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

if __name__ == '__main__':
    app.run(debug=True)

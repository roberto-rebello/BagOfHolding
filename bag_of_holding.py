import os
import flask
from hashlib import sha512
from datetime import datetime

from flask import request

from models import db
from models.user import User
from models.coin import Coin
from models.item import Item
from models.journal import Journal, Entry

app = flask.Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///bag.db'
app.secret_key = os.urandom(24)
db.init_app(app)

# Custom Jinja filter to get environment variable
def get_env(default, env):
    return os.getenv(env, default)

# Add custom filter to Jinja
app.jinja_env.filters["getenv"] = get_env

# Custom filter for date format
@app.template_filter()
def date_format(datetime):
    return datetime.strftime("%d %b %Y")

@app.template_filter()
def datetime_format(datetime):
    return datetime.strftime("%d %b %Y, %H:%M")

### ROUTES
## GENERAL
# Simple login page
@app.route("/login", methods = ["POST", "GET"])
def login():
    if flask.request.method == "POST":

        valid_login = False

        username  = flask.request.form["user"]
        password  = flask.request.form["pass"]

        user  = User.query.filter_by(_username=username).first()
        
        if (user is not None) and (user._password == sha512(password.encode("utf-8")).hexdigest()):
            flask.session["is_admin"] = False
            if user._isAdmin:
                flask.session["is_admin"] = True
            valid_login = True
        else:
            valid_login = False

        if valid_login:
            flask.session["logged_in"] = True
            flask.session["user"] = flask.request.form["user"]
            return flask.redirect("/")
        else:
            flask.session["is_admin"] = False
            flask.session["logged_in"] = False
            flask.session["user"] = ""
            error = "Invalid credentials"
            return flask.render_template("login.html", error=error, login_page=True)

    else:
        return flask.render_template("login.html", login_page=True)

# Simple logout
@app.route("/logout")
def logout():
    flask.session["is_admin"] = False
    flask.session["logged_in"] = False
    flask.session["user"] = ""
    return flask.redirect("/")

# Load main window
@app.route("/", methods = ["GET"])
def index():
    if flask.session.get("logged_in"):
        items = Item.query.order_by(Item._name).all()
        items_value = _getValue(items)
        items_weight = _getWeight(items)

        coins = Coin.query.order_by(Coin._value).all()
        party_gold = _convertDefault(coins)

        return flask.render_template("index.html",
                                     items=items,
                                     items_value=items_value,
                                     items_weight=items_weight,
                                     party_gold=party_gold,
                                     coins=coins,
                                     admin=flask.session["is_admin"])
    else:
        return flask.redirect("/login")

## USERS
# List all current Users
@app.route("/users", methods=["GET"])
def get_users():
    if flask.session.get("logged_in"):
        users = User.query.order_by(User._id).all()

        return flask.render_template("users.html",
                                     users=users,
                                     admin=flask.session["is_admin"])

# Create a new User
@app.route("/users", methods=["POST"])
def create_user():
    if flask.session.get("logged_in"):
        username = flask.request.form["username"].lower()
        password = sha512(flask.request.form["password"].encode("utf-8")).hexdigest()
        is_admin = flask.request.form["isAdmin"] == "Yes"

        new_user = User(username, password, is_admin)

        try:
            db.session.add(new_user)
            db.session.commit()

            return flask.redirect("/users")

        except Exception as e:
            raise

# Update item information
@app.route("/users/update/<int:id>", methods=["POST"])
def update_user(id):
    user = User.query.get_or_404(id)

    user._username = flask.request.form["username"]
    if flask.request.form["password"] != "":
        user._password = sha512(flask.request.form["password"].encode("utf-8")).hexdigest()
    user._isAdmin = flask.request.form["isAdmin"] == "Yes"

    try:
        db.session.commit()
        return flask.redirect("/users")
    except Exception as e:
        raise

# Delete a User
@app.route("/users/delete/<int:id>", methods=["POST"])
def delete_user(id):
    if flask.session.get("logged_in"):
        user = User.query.get_or_404(id)

        try:
            db.session.delete(user)
            db.session.commit()

            return flask.redirect("/users")

        except Exception as e:
            raise

# Change user password
@app.route("/users/<int:id>/password", methods=["POST"])
def change_password(id):
    if flask.session.get("logged_in"):
        new_password = sha512(flask.request.form["password"].encode("utf-8")).hexdigest()

        user = User.query.get_or_404(id)
        user._password = new_password

        try:
            db.session.commit()

            return flask.redirect("/users")

        except Exception as e:
            raise

## ITEMS
# Create a new item
@app.route("/create", methods=["POST"])
def create_item():
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

        no_redirect = request.args.get('noRedirect', False)
        if (no_redirect):
            return ('Created', 201)

        return flask.redirect("/")

    except Exception as e:
        raise

# Remove an item
@app.route("/delete/<int:id>", methods=["POST"])
def delete_item(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return flask.redirect("/")

    except Exception as e:
        raise

# Update item information
@app.route("/update/<int:id>", methods=["POST"])
def update_item(id):
    item = Item.query.get_or_404(id)

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

# Load multi-sell page
@app.route("/sell", methods = ["GET", "POST"])
def sell_index():
    # Query all items and load selling page
    if flask.request.method == "GET":
        if flask.session.get("logged_in"):
            items = Item.query.order_by(Item._name).all()
            items_value = _getValue(items)
            items_weight = _getWeight(items)

            coins = Coin.query.order_by(Coin._value).all()
            party_gold = _convertDefault(coins)

            return flask.render_template("sell.html",
                                         items=items,
                                         items_value=items_value,
                                         items_weight=items_weight,
                                         party_gold=party_gold,
                                         coins=coins,
                                         admin=flask.session["is_admin"])
        else:
            return flask.redirect("/login")
    # Recieves items to be sold, delete or subtract quantity and add total gold to party coins
    else:
        gold = Coin.query.filter_by(_name="Gold").first()

        try:
            for item_id in flask.request.form.keys():
                id = item_id.split("_")[1]

                item = Item.query.get_or_404(id)

                quantity_to_sell = int(flask.request.form[item_id])

                gold._quantity += item._price * quantity_to_sell
                item._quantity -= quantity_to_sell

                if item._quantity <= 0:
                    db.session.delete(item)

            db.session.commit()

            return flask.redirect("/")

        except Exception as e:
            raise

# Sell an item
@app.route("/sell/<int:id>", methods=["POST"])
def sell_item(id):
    try:
        item = Item.query.get_or_404(id)
        gold = Coin.query.filter_by(_name="Gold").first()

        quantity_to_sell = int(flask.request.form["quantity"])

        gold._quantity += item._price * quantity_to_sell
        item._quantity -= quantity_to_sell

        if item._quantity <= 0:
            db.session.delete(item)

        db.session.commit()
        return flask.redirect("/")

    except Exception as e:
        raise

# Create a copy of an item
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

# Increase quantity of an item
@app.route("/add/<int:id>")
def add_item(id):
    item = Item.query.get_or_404(id)

    item._quantity += 1

    try:
        db.session.commit()
        return flask.redirect("/")
    except Exception as e:
        raise

# Decrease quantity of an item
@app.route("/subtract/<int:id>")
def subtract(id):
    item = Item.query.get_or_404(id)

    item._quantity -= 1

    try:
        db.session.commit()
        return flask.redirect("/")
    except Exception as e:
        raise

# Update coin quantity
@app.route("/coin", methods=["POST"])
def update_coin():
    coins = Coin.query.order_by(Coin._value).all()

    for coin in coins:
        coin_quantity = "{}_quantity".format(coin._name)
        coin._quantity = flask.request.form[coin_quantity]

    try:
        db.session.commit()

        return flask.redirect("/")

    except Exception as e:
        raise

## JOURNAL
# Load and Create Journals
@app.route("/journal", methods=["GET", "POST"])
def get_journals():
    if flask.session.get("logged_in"):
        if flask.request.method == "GET":
            journals = list(Journal.query.filter((Journal._user==flask.session.get("user")) | (Journal._is_private==False)))

            return flask.render_template("journal.html",
                                         journals = journals,
                                         user = flask.session.get("user"),
                                         admin=flask.session["is_admin"])

        elif flask.request.method == "POST":
            new_journal = Journal(flask.request.form["author"],
                                  flask.request.form["title"],
                                  flask.request.form["is_private"]=="Yes",
                                  flask.session.get("user"))

            try:
                db.session.add(new_journal)
                db.session.commit()
                return flask.redirect("/journal")

            except Exception as e:
                raise

    else:
        return flask.redirect("/login")

# Acess or Create a new journal entry
@app.route("/journal/<int:id>", methods=["GET", "POST"])
def get_entries(id):
    if flask.session.get("logged_in"):
        journal = Journal.query.get_or_404(id)
        entries = journal.entries

        if flask.request.method == "GET":
            return flask.render_template("entries.html",
                                         journal = journal,
                                         entries = entries,
                                         user = flask.session.get("user"),
                                         admin=flask.session["is_admin"])

        elif flask.request.method == "POST":
            new_entry = Entry(journal,
                              flask.request.form["author"],
                              flask.request.form["title"],
                              flask.request.form["body"],
                              flask.request.form["game_date"],
                              flask.request.form["location"])

            try:
                db.session.commit()
                return flask.redirect("/journal/{}".format(id))

            except Exception as e:
                raise
    else:
        return flask.redirect("/login")

# Create a journal entry
@app.route("/journal/<int:id>/entry", methods=["GET", "POST"])
def create_entry(id):
    if flask.session.get("logged_in"):
        journal = Journal.query.get_or_404(id)

        if flask.request.method == "GET":
            entry = Entry(journal, "", "", "", "", "")

            return flask.render_template("entry.html",
                                         journal = journal,
                                         entry = entry,
                                         user = flask.session.get("user"),
                                         admin=flask.session["is_admin"])

        elif flask.request.method == "POST":
            entry = Entry(journal,
                          flask.request.form["author"],
                          flask.request.form["title"],
                          flask.request.form["body"],
                          flask.request.form["game_date"],
                          flask.request.form["location"])

            try:
                db.session.commit()
                return flask.redirect("/journal/{}".format(id))

            except Exception as e:
                raise
    else:
        return flask.redirect("/login")

# Acess or Edit a journal entry
@app.route("/journal/<int:id>/entry/<int:entry_id>", methods=["GET", "POST"])
def update_entry(id, entry_id):
    if flask.session.get("logged_in"):
        journal = Journal.query.get_or_404(id)
        entry = Entry.query.get_or_404(entry_id)

        if flask.request.method == "GET":
            return flask.render_template("entry.html",
                                         journal = journal,
                                         entry = entry,
                                         user = flask.session.get("user"),
                                         admin=flask.session["is_admin"])

        elif flask.request.method == "POST":
            entry._author = flask.request.form["author"]
            entry._title = flask.request.form["title"]
            entry._body = flask.request.form["body"]
            entry._game_date = flask.request.form["game_date"]
            entry._location = flask.request.form["location"]
            entry._edit_date = datetime.utcnow()

            try:
                db.session.commit()
                return flask.redirect("/journal/{}".format(id))

            except Exception as e:
                raise
    else:
        return flask.redirect("/login")

# Acess or Edit a journal entry
@app.route("/journal/<int:id>/entry/<int:entry_id>/delete", methods=["POST"])
def delete_entry(id, entry_id):
    if flask.session.get("logged_in"):
        entry = Entry.query.get_or_404(entry_id)

        try:
            return_url = "/journal/{}".format(id)

            db.session.delete(entry)

            journal = Journal.query.get_or_404(id)
            if len(journal.entries) == 0:
                db.session.delete(journal)
                return_url = "/journal"

            db.session.commit()

            return flask.redirect(return_url)

        except Exception as e:
            raise

    else:
        return flask.redirect("/login")


## PRIVATE FUNCTIONS
# Get total value of items
def _getValue(items):
    total_value = 0.0
    for item in items:
        total_value += (item._price * item._quantity)

    return round(total_value, 1)

# Get total weight of items
def _getWeight(items):
    total_weight = 0.0
    for item in items:
        total_weight += (item._weight * item._quantity)

    return round(total_weight, 1)

# Convert coins to defaut value
def _convertDefault(coins, default="Gold"):
    default_value = Coin.query.filter_by(_name=default).first()._value

    gold = 0.0
    for coin in coins:
        gold += coin._value * coin._quantity

    return round(gold/default_value, 1)

if __name__ == '__main__':
    app.run(debug=True)

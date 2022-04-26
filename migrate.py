from hashlib import sha512
from flask_migrate import Migrate
from bag_of_holding import app, db, Coin, User

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        copper = Coin("Copper", 1, 0)
        silver = Coin("Silver", 10, 0)
        gold = Coin("Gold", 100, 0)
        platinum = Coin("Platinum", 1000, 0)

        admin = User("admin", sha512("admin".encode("utf-8")).hexdigest(), is_admin=True)

        db.session.add(copper)
        db.session.add(silver)
        db.session.add(gold)
        db.session.add(platinum)

        db.session.add(admin)

        db.session.commit()

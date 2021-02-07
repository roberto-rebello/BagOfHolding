from flask_migrate import Migrate
from bag_of_holding import app, db, Coin

migrate = Migrate(app, db)

if __name__ == '__main__':
    db.create_all()

    copper = Coin("Copper", 1, 0)
    silver = Coin("Silver", 10, 0)
    gold = Coin("Gold", 100, 0)
    platinum = Coin("Platinum", 1000, 0)

    db.session.add(copper)
    db.session.add(silver)
    db.session.add(gold)
    db.session.add(platinum)

    db.session.commit()

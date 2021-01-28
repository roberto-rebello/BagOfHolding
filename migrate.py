from flask_migrate import Migrate
from bag_of_holding import app, db

migrate = Migrate(app, db)

if __name__ == '__main__':
    db.create_all()

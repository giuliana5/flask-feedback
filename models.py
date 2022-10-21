from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to the db."""

    db.app = app
    db.init_app

    with app.app_context():
        db.create_all()

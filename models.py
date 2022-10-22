from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to the db."""

    db.app = app
    db.init_app

    with app.app_context():
        db.create_all()


class User(db.Model):
    """Stores user info."""

    __tablename__ = "users"

    username = db.Column(db.Text(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text(50), nullable=False, unique=True)
    first_name = db.Column(db.Text(30), nullable=False)
    last_name = db.Column(db.Text(30), nullable=False)

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the db."""

    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()


class User(db.Model):
    """Stores user info."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed pwd & return user."""

        hashed = bcrypt.generate_password_hash(pwd)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that the user exists & the password is correct."""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return False

class Feedback(db.Model):
    """Stores user feedback."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable=False)

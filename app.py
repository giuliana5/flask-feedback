from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///exercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    """Redirects to registration page."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Goes to form & retrieves form data to register a new user."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Displays login form and logs the user in."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.username}!")
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ['Invalid username/password.']
            return render_template("login.html", form=form)

    else:
        return render_template("login.html", form=form)

@app.route("/users/<username>", methods=["GET", "POST"])
def user_page(username):
    """Goes to user's page."""

    if session["username"] != username:
        return redirect("/")
    
    user = User.query.get_or_404(username)
    all_feedback = Feedback.query.filter_by(username=username).all()

    return render_template("user.html", all_feedback=all_feedback, user=user)

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Display feedback form & add new feedback."""

    if session["username"] != username:
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        flash("Feedback Posted!")
        return redirect(f"/users/{username}")
    
    else:
        return render_template("feedback-new.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Update posted feedback."""

    feedback = Feedback.query.get_or_404(feedback_id)

    if session["username"] != feedback.username:
        return redirect("/")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback Updated!")
        return redirect(f"/users/{feedback.username}")
    
    return render_template("feedback-edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback from db."""

    feedback = Feedback.query.get_or_404(feedback_id)

    if session["username"] != feedback.username:
        return redirect("/")

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes user from db."""

    if session["username"] != username:
        return redirect("/") 

    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()   
    session.pop("username")

    return redirect("/")
    
@app.route("/logout", methods=["POST"])
def logout_user():
    """Logs the user out."""

    session.pop('username')

    return redirect("/")

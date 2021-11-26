import functools

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask import g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import date

from .models.pacjent import Pacjent
from .models.pracownik import Pracownik
from .models.usluga_wizyta import Usluga_Wizyta
from .models.usluga import Usluga
from .models.wizyta import Wizyta

from . import db

auth = Blueprint("auth", __name__)

#TO DO
def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

#TO DO
@auth.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            db.session.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@auth.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        pesel = request.form["pesel"]
        birthdate = request.form["birthdate"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Login wymagany."
        elif not password:
            error = "Hasło wymagane."
        elif not name:
            error = "Imię wymagane."
        elif not surname:
            error = "Nazisko wymagane."
        elif not pesel:
            error = "PESEL wymagany."
        elif not phone:
            error = "Telefon wymagany."
        

        if error is None:
            try:
                db.session.add(Pacjent(imie=name, pesel=pesel, data_rejestracji=date.today(), login=username, haslo=generate_password_hash(password)))
                #    db.session.execute(
                #        "INSERT INTO user (username, password) VALUES (?, ?)",
                #        (username, generate_password_hash(password)),
                #    )
                db.session.commit()
            except db.session.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"Login {username} jest zajęty."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@auth.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        user = db.session.query(Pacjent).filter(Pacjent.login == username).first()
        #user = db.session.execute(
        #    "SELECT * FROM user WHERE username = ?", (username,)
        #).fetchone()
        doc = db.session.query(Pracownik).filter(Pracownik.login == username).first()

        if user is None or doc is None:
            error = "Niepoprawny login."
        elif not check_password_hash(user[login], password) or not check_password_hash(doc[login], password):
            error = "Niepoprawne hasło"
        
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            if user is None:
                session["user_id"] = doc["id"]
                return redirect(url_for("index_pracownik"))
            else:
                session["user_id"] = user["id"]
                return redirect(url_for("index_pacjent"))

        flash(error)

    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
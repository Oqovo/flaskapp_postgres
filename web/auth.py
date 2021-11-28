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
            db.session.query(Pacjent).filter(Pacjent.id == user_id).first()
            #db.session.execute("SELECT * FROM pacjent WHERE id = ?", (user_id,)).fetchone()
        )
    if g.user is None:
        g.user = (
            db.session.query(Pracownik).filter(Pracownik.id == user_id).first()
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
            error = "Nazwisko wymagane."
        elif not pesel:
            error = "PESEL wymagany."
        elif not phone:
            error = "Telefon wymagany."
        

        if error is None:
            try:
                db.session.add(Pacjent(imie=name, nazwisko = surname, pesel=pesel, numer_telefonu = phone, data_rejestracji=date.today(), login=username, haslo=generate_password_hash(password)))
                #    db.session.execute(
                #        "INSERT INTO Pacjent (username, password) VALUES (?, ?)",
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
    print("*** Rozpoczynamy login")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        user = db.session.query(Pacjent).filter(Pacjent.login == username).first()
        #user = db.session.execute(
        #    "SELECT * FROM user WHERE username = ?", (username,)
        #).fetchone()
        doc = db.session.query(Pracownik).filter(Pracownik.login == username).first()


        if (user is None) and (doc is None):
            error = "Niepoprawny login."
        elif ((user is not None) and (not check_password_hash(user.haslo, password))):
            error = "Niepoprawne hasło"
        elif((doc is not None) and (not check_password_hash(doc.haslo, password))):
            error = "Niepoprawne hasło"
        
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            if user is None:
                session["user_id"] = doc.id 
                session["tablename"] = doc.__tablename__
                print(session)
                return redirect(url_for("views.index_pracownik"))
            else:
                session["user_id"] = user.id
                session["tablename"] = user.__tablename__
                print(session)
                return redirect(url_for("views.index_pacjent"))
        print("******", error)
        flash(error)

    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("views.index"))
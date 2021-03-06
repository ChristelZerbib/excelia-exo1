from bottle import route, run, template, request, response, redirect
import sqlite3
import sys
from helpers import somme, generate_cookie_value


@route("/hello/<name>")
def hello(name):
    response.set_cookie("name", name, path="/")
    return template("<b>Hello {{name}}</b>!", name=name)


@route("/index")
def index():
    name = request.get_cookie("name")
    return template("<b>Salut {{name}} !</b>", name=name)


@route("/signup", method=["GET", "POST"])
def signup():
    if request.method == "GET":
        return template("signup_template")
    else:
        username = request.forms.username
        email = request.forms.email
        password = request.forms.password
        if username == "":
            return {"error": True, "message": "Il manque un nom d'utilisateur"}
        conn = sqlite3.connect("fb.db")
        cursor = conn.cursor()

        cursor.execute(
            f"INSERT INTO facebook (username, email, password) VALUES('{username}', '{email}', '{password}')"  # noqa : E501
        )
        conn.commit()
        return {"error": False, "message": "Utilisateur enregistré"}


@route("/login", method=["GET", "POST"])
def login():
    if request.method == "GET":
        return template("login_template")
    else:
        username = request.forms.username
        password = request.forms.password
        conn = sqlite3.connect("fb.db")
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT password FROM facebook WHERE username ='{username}'"
        )  # noqa : E501
        db_password = cursor.fetchone()

        if db_password[0] == "":
            return {"error": True, "message": "Utilisateur inconnu"}
        if db_password[0] != password:
            return {"error": True, "message": "Mot de passe erroné"}
        else:
            cookie_value = generate_cookie_value()
            cursor.execute(
                f"UPDATE facebook SET cookie = '{cookie_value}' WHERE username = '{username}'"  # noqa : E501
            )
            conn.commit()
            response.set_cookie("fb_session", cookie_value, path="/")
            redirect("/user")


@route("/user")
def user_info():
    fb_session = request.get_cookie("fb_session")
    conn = sqlite3.connect("fb.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM facebook WHERE cookie ='{fb_session}'")
    result = cursor.fetchone()
    print(result)

    if result is None:
        redirect("/login")
    else:
        return template("user_info", username=result[1], email=result[2])


@route("/addition/<a>/<b>")
def addition(a, b):
    resultat = somme(a, b)
    return template(
        "<b>La somme de {{a}} et de {{b}} est {{resultat}} !</b>",
        a=a,
        b=b,
        resultat=resultat,
    )  # noqa : E501


run(host="0.0.0.0", port=sys.argv[1], reloader=True)

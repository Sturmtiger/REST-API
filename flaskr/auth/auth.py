import functools

from flask import abort
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flaskr.db import get_db
from flaskr.auth.queries import (
    create_user, get_user_by_id, get_user_by_username
)


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    db = get_db()
    user = get_user_by_username(db, username)
    if user is None or not check_password_hash(user['password'], password):
        return False

    session.clear()
    session["user_id"] = user["id"]
    return True


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(get_db(), user_id)


@bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    db = get_db()
    error = None

    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')

    if get_user_by_username(db, username) is not None:
        error = "User {0} is already registered.".format(username)

    if error is None:
        # the name is available, store it in the database
        create_user(db, username, password)
        return Response(
            response='Registration is successful', 
            status=200,
            )
    abort(409, "User {} already exists".format(username))


@bp.route("/logout")
@auth.login_required
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return Response(
        response='Logged out',
        status=401,
        )

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("user_req", __name__)


@bp.route("/")
def index():
    """Show all the requests, most recent first."""
    db = get_db()
    reqs = db.execute(
        "SELECT r.id, req_date, req_time, location, priority, capacity, created, user_id, username"
        " FROM req r JOIN user u ON r.user_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("user_req/index.html", reqs=reqs)


def get_req (id, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    req = (
        get_db().execute(
            "SELECT r.id, req_date, req_time, location, priority, capacity, created, user_id, username"
            " FROM req r JOIN user u ON r.user_id = u.id"
            " WHERE r.id = ?",
            (id,)
            ).fetchone()
    )

    if req is None:
        abort(404, "request id {0} does not exist".format(id))

    if check_author and req["user_id"] != g.user["id"]:
        abort(403)

    return req


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        req_date = request.form["req_date"]
        req_time = request.form["req_time"]
        location = request.form["location"]
        priority = request.form["priority"]
        capacity = request.form["capacity"]
        error = None

        if not req_date:
            error = "date is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO req (req_date, req_time, location, priority, capacity, user_id)" "VALUES (?, ?, ?, ?, ?, ?)",
                (req_date, req_time, location, priority, capacity, g.user["id"])
            )
            db.commit()
            return redirect(url_for("user_req.index"))

    return render_template("user_req/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    req = get_req(id)

    if request.method == "POST":
        req_date = request.form["req_date"]
        req_time = request.form["req_time"]
        location = request.form["location"]
        priority = request.form["priority"]
        capacity = request.form["capacity"]
        error = None

        if not req_date:
            error = "date is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE req SET req_date = ?, req_time = ?, location = ?, priority = ?, capacity = ? WHERE id = ?", (req_date, req_time, location, priority, capacity, id)
            )
            db.commit()
            return redirect(url_for("user_req.index"))

    return render_template("user_req/update.html", req=req)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_req(id)
    db = get_db()
    db.execute("DELETE FROM req WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("user_req.index"))

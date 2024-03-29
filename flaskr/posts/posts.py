from flask import jsonify
from flask import Blueprint
from flask import request
from flask import Response
from werkzeug.exceptions import abort

from flaskr.db import get_db
from flaskr.posts.queries import (create_post, delete_post,
                                 get_post, update_post, post_list)
from flaskr.auth.queries import get_user_by_username
from flaskr.auth.auth import auth


bp = Blueprint("posts", __name__)


@bp.route("/posts/", methods=["GET"])
@auth.login_required
def posts():
    """Show all the posts, most recent first."""
    db = get_db()
    posts_sql = post_list(db)

    if not posts_sql:
        abort(404, 'No posts available')

    posts = [dict(post) for post in posts_sql]
    return jsonify(posts)


@bp.route("/posts/<int:id>/", methods=["GET"])
@auth.login_required
def post(id):
    """Show post"""
    db = get_db()
    post = check_post(id, False)

    post = dict(post)
    return jsonify(post)


@bp.route("/posts/", methods=["POST"])
@auth.login_required
def create():
    """Create post"""
    if request.is_json:
        request_data = request.get_json()
        title = request_data.get('title', '').strip()
        body = request_data.get('body', '').strip()
        if not title or not body:
            abort(400, '(title, body) properties must not be empty')

        db = get_db()
        current_user = get_user_by_username(db, request.authorization["username"])
        create_post(db, title, body, current_user["id"])

        return Response(
            response='Post has been created',
            status=201,
            )
    else:
        abort(400, 'JSON must be passed')


@bp.route("/posts/<int:id>/", methods=["PUT"])
def update(id):
    """Update a post if the current user is the author."""
    check_post(id)

    if request.is_json:
        request_data = request.get_json()
        title = request_data.get('title', '').strip()
        body = request_data.get('body', '').strip()
        if not title or not body:
            abort(400, '(title, body) properties must not be empty')

        db = get_db()
        update_post(db, title, body, id)
        return Response(
            response='Post has been updated', 
            status=200
            )
    else:
        abort(400, 'JSON must be passed')


@bp.route("/posts/<int:id>/", methods=["DELETE"])
def delete(id): 
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    check_post(id)

    db = get_db()
    delete_post(db, id)

    return Response('Post has been deleted', 200)


def check_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    db = get_db()

    post = get_post(db, id)
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    current_user = get_user_by_username(db, request.authorization["username"])
    if check_author and post["author_id"] != current_user["id"]:
        abort(403)

    return post

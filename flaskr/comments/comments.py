from flask import jsonify
from flask import Blueprint
from flask import g
from flask import request
from flask import Response
from werkzeug.exceptions import abort

from flaskr.db import get_db
from flaskr.comments.queries import (get_list_of_post_comments, get_comment_of_post, delete_comment_of_post,
                                    create_comment_for_post, update_comment_of_post)
from flaskr.auth.auth import auth

bp = Blueprint("comments", __name__)


# @bp.route("/posts/<int:id>/comments/", methods=["GET"])
@bp.route("/posts/<int:id>/comments/", methods=["GET"])
@auth.login_required
def comments(id):
    """Show all post comments, most recent first."""
    db = get_db()
    comments_sql = get_list_of_post_comments(db, id)

    if not comments_sql:
        abort(404, 'No comments available')
    
    comments = [dict(comment) for comment in comments_sql]
    return jsonify(comments)


@bp.route("/posts/<int:post_id>/comments/<int:comment_id>/", methods=["GET"])
@auth.login_required
def comment(post_id, comment_id):
    """Show specific post comment"""
    check_comment(post_id, comment_id, False)

    db = get_db()
    comment_sql = get_comment_of_post(db, post_id, comment_id)

    comment = dict(comment_sql)
    return jsonify(comment)


@bp.route("/posts/<int:id>/comments/", methods=["POST"])
@auth.login_required
def create(id):
    """Create comment for specific post"""
    request_data = request.get_json()
    text = request_data.get('text')

    db = get_db()
    create_comment_for_post(db, g.user["id"], id, text)
    return Response(
        response='Comment has been created',
        status=201,
        )


@bp.route("/posts/<int:post_id>/comments/<int:comment_id>/", methods=["PUT"])
@auth.login_required
def update(post_id, comment_id):
    """Update specific post comment if current user is the author"""
    check_comment(post_id, comment_id)

    request_data = request.get_json()
    text = request_data.get('text')

    db = get_db()
    update_comment_of_post(db, post_id, comment_id, text)

    return Response(
        response='Commet has been updated',
        status=200,
        )


@bp.route("/posts/<int:post_id>/comments/<int:comment_id>/", methods=["DELETE"])
@auth.login_required
def delete(post_id, comment_id):
    """Delete specific post comment if current user is the author"""
    check_comment(post_id, comment_id)

    db = get_db()
    delete_comment_of_post(db, post_id, comment_id)

    return Response(
        response='Comment has been deleted',
        status=200,
        )


def check_comment(post_id, comment_id, check_author=True):
    """Get a comment and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param post_id: id of post 
    :param comment_id: id of comment to get
    :param check_author: require the current user to be the author
    :return: the comment with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """

    db = get_db()
    comment = get_comment_of_post(db, post_id, comment_id)
    if comment is None:
        abort(404, "Comment id {0} doesn't exist.".format(comment_id))

    if check_author and comment["author_id"] != g.user["id"]:
        abort(403)

    return comment

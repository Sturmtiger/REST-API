

def get_list_of_post_comments(db, id):
    return db.execute(
            "SELECT c.text, c.created, c.id, c.author_id, " 
            "u.username "
            "FROM comment c "
            "INNER JOIN user u "
            "ON c.author_id = u.id "
            "WHERE c.post_id = ? "
            "ORDER BY c.created DESC",
            (id,),
        ).fetchall()


def get_comment_of_post(db, post_id, comment_id):
    return db.execute(
        "SELECT c.text, c.created, c.id, c.author_id, "
        "u.username "
        "FROM comment c "
        "INNER JOIN user u "
        "ON c.author_id = u.id "
        "WHERE c.post_id = ? AND c.id = ?",
        (post_id, comment_id),
    ).fetchone()


def update_comment_of_post(db, post_id, comment_id, text):
    db.execute(
        "UPDATE comment "
        "SET text = ? "
        "WHERE post_id = ? AND id = ?",
        (text, post_id, comment_id),
    )
    db.commit()


def delete_comment_of_post(db, post_id, comment_id):
    db.execute(
        "DELETE FROM comment "
        "WHERE post_id = ? AND id = ?",
        (post_id, comment_id),
    )
    db.commit()


def create_comment_for_post(db, author_id, post_id, text):
    db.execute(
        "INSERT INTO comment (author_id, post_id, text) VALUES (?, ?, ?)",
        (author_id, post_id, text),
    )
    db.commit()
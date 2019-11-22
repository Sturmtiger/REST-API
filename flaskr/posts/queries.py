

def post_list(db):
    return db.execute(
        # TODO: sql - выбрать поля:
        # id, title, body, created, author_id, username
        # из таблицы post и таблицы user (они связаны)
        # и отсортировать по дате создания по убыванию
        "SELECT p.title, p.body, p.created, p.id, "
        "p.author_id, u.username "
        "FROM post p INNER JOIN user u "
        "ON p.author_id = u.id "
        "ORDER BY p.created DESC"
    ).fetchall()


def get_post(db, id):
    return db.execute(
            "SELECT p.title, p.body, p.created, p.id, "
            "p.author_id, u.username "
            "FROM post p JOIN user u "
            "ON p.author_id = u.id "
            "WHERE p.id = ?",
            (id,),
        ).fetchone()


def create_post(db, title, body, author_id):
    db.execute(
        "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
        (title, body, author_id),
    )
    db.commit()


def update_post(db, title, body, id):
    db.execute(
        # TODO: sql - обновить поля title, body у post с переданным ид
        "UPDATE post "
        "SET title = ?, body = ? "
        "WHERE id = ?",
        (title, body, id)
    )
    db.commit()


def delete_post(db, id):
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()

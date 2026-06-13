from server.database import Database


class FeedManager:

    def __init__(self):
        self.db = Database()

    def create_post(
        self,
        username,
        content
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO posts(
                username,
                content
            )
            VALUES(?,?)
            """,
            (
                username,
                content
            )
        )

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "message": "Post berhasil dibuat"
        }

    def get_feed(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                content,
                created_at
            FROM posts
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        posts = []

        for row in rows:

            posts.append(
                {
                    "id": row[0],
                    "username": row[1],
                    "content": row[2],
                    "created_at": row[3]
                }
            )

        return {
            "status": "success",
            "posts": posts
        }

    def like_post(
        self,
        post_id,
        username
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM likes
            WHERE post_id=?
            AND username=?
            """,
            (
                post_id,
                username
            )
        )

        existing = cursor.fetchone()

        # unlike
        if existing:

            cursor.execute(
                """
                DELETE FROM likes
                WHERE post_id=?
                AND username=?
                """,
                (
                    post_id,
                    username
                )
            )

            conn.commit()
            conn.close()

            return {
                "status": "success",
                "liked": False,
                "message": "Unlike berhasil"
            }

        # like
        cursor.execute(
            """
            INSERT INTO likes(
                post_id,
                username
            )
            VALUES(?,?)
            """,
            (
                post_id,
                username
            )
        )

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "liked": True,
            "message": "Like berhasil"
        }

    def has_liked(
        self,
        post_id,
        username
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM likes
            WHERE post_id=?
            AND username=?
            """,
            (
                post_id,
                username
            )
        )

        result = cursor.fetchone()

        conn.close()

        return {
            "status": "success",
            "liked": result is not None
        }

    def get_like_count(
        self,
        post_id
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM likes
            WHERE post_id=?
            """,
            (post_id,)
        )

        count = cursor.fetchone()[0]

        conn.close()

        return {
            "status": "success",
            "count": count
        }

    def comment_post(
        self,
        post_id,
        username,
        comment
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO comments(
                post_id,
                username,
                comment
            )
            VALUES(?,?,?)
            """,
            (
                post_id,
                username,
                comment
            )
        )

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "message": "Comment berhasil"
        }

    def get_comments(
        self,
        post_id
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                username,
                comment,
                created_at
            FROM comments
            WHERE post_id=?
            ORDER BY id ASC
            """,
            (post_id,)
        )

        rows = cursor.fetchall()

        conn.close()

        comments = []

        for row in rows:

            comments.append(
                {
                    "username": row[0],
                    "comment": row[1],
                    "created_at": row[2]
                }
            )

        return {
            "status": "success",
            "comments": comments
        }
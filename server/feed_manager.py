import base64
import os
import time

from server.database import Database


class FeedManager:
    ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    MAX_IMAGE_BYTES = 8 * 1024 * 1024

    def __init__(self):
        self.db = Database()

    def _sanitize_filename(self, filename):
        name = os.path.basename(filename or "post_image")
        safe_chars = []

        for char in name:
            if char.isalnum() or char in (".", "_", "-"):
                safe_chars.append(char)
            elif char.isspace():
                safe_chars.append("_")

        safe_name = "".join(safe_chars).strip("._")
        return safe_name or "post_image"

    def _validate_image_extension(self, filename):
        _, extension = os.path.splitext(filename.lower())
        return extension in self.ALLOWED_IMAGE_EXTENSIONS

    def _save_post_image(self, username, image_filename, image_data):
        if not image_data:
            return None, None

        if not image_filename:
            raise ValueError("Nama file gambar tidak valid")

        if not self._validate_image_extension(image_filename):
            raise ValueError("Format gambar tidak didukung. Gunakan PNG, JPG, JPEG, GIF, BMP, atau WEBP")

        try:
            image_bytes = base64.b64decode(image_data.encode("ascii"), validate=True)
        except Exception as exc:
            raise ValueError("Data gambar tidak valid") from exc

        if len(image_bytes) > self.MAX_IMAGE_BYTES:
            raise ValueError("Ukuran gambar maksimal 8 MB")

        upload_dir = os.path.join("uploads", "posts")
        os.makedirs(upload_dir, exist_ok=True)

        safe_filename = self._sanitize_filename(image_filename)
        safe_username = self._sanitize_filename(username).replace(".", "_")
        stored_name = f"{int(time.time() * 1000)}_{safe_username}_{safe_filename}"
        destination_path = os.path.join(upload_dir, stored_name)

        with open(destination_path, "wb") as image_file:
            image_file.write(image_bytes)

        return stored_name, destination_path

    def create_post(self, username, content, image_filename=None, image_data=None):
        content = (content or "").strip()

        if not content and not image_data:
            return {
                "status": "error",
                "message": "Post harus berisi teks atau foto"
            }

        try:
            stored_image_name, stored_image_path = self._save_post_image(
                username,
                image_filename,
                image_data
            )
        except ValueError as exc:
            return {
                "status": "error",
                "message": str(exc)
            }

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO posts(username, content, image_filename, image_path)
                VALUES(?,?,?,?)
                """,
                (username, content, stored_image_name, stored_image_path)
            )

            conn.commit()

            return {
                "status": "success",
                "message": "Post berhasil dibuat"
            }
        except Exception as exc:
            conn.rollback()

            if stored_image_path and os.path.exists(stored_image_path):
                os.remove(stored_image_path)

            return {
                "status": "error",
                "message": str(exc)
            }
        finally:
            conn.close()

    def _read_image_as_base64(self, image_path):
        if not image_path or not os.path.exists(image_path):
            return None

        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("ascii")
        except Exception:
            return None

    def get_feed(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, content, image_filename, image_path, created_at
            FROM posts
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()
        conn.close()

        posts = []

        for row in rows:
            image_path = row[4]

            posts.append({
                "id": row[0],
                "username": row[1],
                "content": row[2],
                "image_filename": row[3],
                "image_path": image_path,
                "image_data": self._read_image_as_base64(image_path),
                "created_at": row[5]
            })

        return {
            "status": "success",
            "posts": posts
        }

    def like_post(self, post_id, username):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM likes WHERE post_id=? AND username=?",
            (post_id, username)
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "DELETE FROM likes WHERE post_id=? AND username=?",
                (post_id, username)
            )
            conn.commit()
            conn.close()
            return {
                "status": "success",
                "liked": False,
                "message": "Unlike berhasil"
            }

        cursor.execute(
            "INSERT INTO likes(post_id, username) VALUES(?,?)",
            (post_id, username)
        )
        conn.commit()
        conn.close()

        return {
            "status": "success",
            "liked": True,
            "message": "Like berhasil"
        }

    def has_liked(self, post_id, username):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM likes WHERE post_id=? AND username=?",
            (post_id, username)
        )
        result = cursor.fetchone()
        conn.close()

        return {
            "status": "success",
            "liked": result is not None
        }

    def get_like_count(self, post_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM likes WHERE post_id=?",
            (post_id,)
        )
        count = cursor.fetchone()[0]
        conn.close()

        return {
            "status": "success",
            "count": count
        }

    def comment_post(self, post_id, username, comment):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO comments(post_id, username, comment) VALUES(?,?,?)",
            (post_id, username, comment)
        )

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "message": "Comment berhasil"
        }

    def get_comments(self, post_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, comment, created_at FROM comments WHERE post_id=? ORDER BY id ASC",
            (post_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        comments = []

        for row in rows:
            comments.append({
                "username": row[0],
                "comment": row[1],
                "created_at": row[2]
            })

        return {
            "status": "success",
            "comments": comments
        }

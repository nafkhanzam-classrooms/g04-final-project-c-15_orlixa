import hashlib
from server.database import Database


class AuthManager:
    def __init__(self):
        self.db = Database()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, self.hash_password(password))
            )
            conn.commit()
            return {
                "status": "success",
                "message": "Register berhasil"
            }
        except Exception:
            return {
                "status": "error",
                "message": "Username sudah digunakan"
            }
        finally:
            conn.close()

    def login(self, username, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            return {
                "status": "error",
                "message": "User tidak ditemukan"
            }

        hashed = self.hash_password(password)

        if hashed != result[0]:
            return {
                "status": "error",
                "message": "Password salah"
            }

        return {
            "status": "success",
            "message": "Login berhasil"
        }

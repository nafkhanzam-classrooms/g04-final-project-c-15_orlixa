import os
import shutil


class PrivateManager:
    """Menangani seluruh logic private chat dan private file transfer."""

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def send_private_message(self, packet):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        try:
            cursor.execute(
                "INSERT INTO messages(sender, receiver, message) VALUES(?,?,?)",
                (
                    packet["sender"],
                    packet["receiver"],
                    packet["message"]
                )
            )
            conn_db.commit()
            return {
                "status": "success",
                "message": "Pesan terkirim"
            }
        except Exception as e:
            conn_db.rollback()
            self.logger.error(str(e))
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            conn_db.close()

    def get_inbox_messages(self, username):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        cursor.execute(
            """
            SELECT sender, message, created_at
            FROM messages
            WHERE receiver=?
            ORDER BY id DESC
            """,
            (username,)
        )

        rows = cursor.fetchall()
        conn_db.close()

        messages = []

        for row in rows:
            messages.append({
                "sender": row[0],
                "message": row[1],
                "created_at": row[2]
            })

        return {
            "status": "success",
            "messages": messages
        }

    def get_conversation(self, user1, user2):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        cursor.execute(
            """
            SELECT sender, receiver, message, created_at
            FROM messages
            WHERE (sender=? AND receiver=?)
               OR (sender=? AND receiver=?)
            ORDER BY id ASC
            """,
            (user1, user2, user2, user1)
        )

        rows = cursor.fetchall()
        conn_db.close()

        messages = []

        for row in rows:
            messages.append({
                "sender": row[0],
                "receiver": row[1],
                "message": row[2],
                "created_at": row[3]
            })

        return {
            "status": "success",
            "messages": messages
        }

    def send_private_file(self, packet):
        os.makedirs("uploads", exist_ok=True)

        source_path = packet["filepath"]
        filename = packet["filename"]
        destination_path = os.path.join("uploads", filename)

        try:
            shutil.copy(source_path, destination_path)

            conn_db = self.db.get_connection()
            cursor = conn_db.cursor()

            cursor.execute(
                "INSERT INTO file_messages(sender, receiver, filename, filepath) VALUES(?,?,?,?)",
                (
                    packet["sender"],
                    packet["receiver"],
                    filename,
                    destination_path
                )
            )

            cursor.execute(
                "INSERT INTO messages(sender, receiver, message) VALUES(?,?,?)",
                (
                    packet["sender"],
                    packet["receiver"],
                    f"[FILE] {filename}"
                )
            )

            conn_db.commit()
            conn_db.close()

            return {
                "status": "success",
                "message": f"File {filename} berhasil dikirim"
            }

        except Exception as e:
            self.logger.error(str(e))
            return {
                "status": "error",
                "message": str(e)
            }

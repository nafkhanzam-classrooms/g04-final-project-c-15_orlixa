import os
import shutil
import time


class RoomManager:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def create_room(self, username, room_name):
        room_name = room_name.strip()

        if not room_name:
            return {
                "status": "error",
                "message": "Nama room tidak boleh kosong"
            }

        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        try:
            cursor.execute(
                "SELECT id FROM rooms WHERE name=?",
                (room_name,)
            )

            if cursor.fetchone():
                return {
                    "status": "error",
                    "message": "Room sudah ada"
                }

            cursor.execute(
                "INSERT INTO rooms(name, created_by) VALUES(?, ?)",
                (room_name, username)
            )
            room_id = cursor.lastrowid

            cursor.execute(
                "INSERT OR IGNORE INTO room_members(room_id, username) VALUES(?, ?)",
                (room_id, username)
            )

            conn_db.commit()
            self.logger.info(f"Room created: {room_name} by {username}")

            return {
                "status": "success",
                "message": "Room berhasil dibuat",
                "room_id": room_id
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

    def list_rooms(self):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        cursor.execute("""
            SELECT
                r.id,
                r.name,
                r.created_by,
                r.created_at,
                COUNT(m.username) AS total_members
            FROM rooms r
            LEFT JOIN room_members m ON r.id = m.room_id
            GROUP BY r.id
            ORDER BY r.id DESC
        """)

        rows = cursor.fetchall()
        conn_db.close()

        rooms = []

        for row in rows:
            rooms.append({
                "id": row[0],
                "name": row[1],
                "created_by": row[2],
                "created_at": row[3],
                "members": row[4]
            })

        return {
            "status": "success",
            "rooms": rooms
        }

    def join_room(self, username, room_id):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        try:
            cursor.execute(
                "SELECT id FROM rooms WHERE id=?",
                (room_id,)
            )

            if not cursor.fetchone():
                return {
                    "status": "error",
                    "message": "Room tidak ditemukan"
                }

            cursor.execute(
                "INSERT OR IGNORE INTO room_members(room_id, username) VALUES(?, ?)",
                (room_id, username)
            )

            conn_db.commit()
            self.logger.info(f"{username} joined room {room_id}")

            return {
                "status": "success",
                "message": "Berhasil join room"
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

    def leave_room(self, username, room_id):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        try:
            cursor.execute(
                "DELETE FROM room_members WHERE room_id=? AND username=?",
                (room_id, username)
            )

            conn_db.commit()
            self.logger.info(f"{username} left room {room_id}")

            return {
                "status": "success",
                "message": "Berhasil keluar dari room"
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

    def send_room_message(self, room_id, sender, message):
        message = message.strip()

        if not message:
            return {
                "status": "error",
                "message": "Pesan tidak boleh kosong"
            }

        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        try:
            cursor.execute(
                "SELECT id FROM room_members WHERE room_id=? AND username=?",
                (room_id, sender)
            )

            if not cursor.fetchone():
                return {
                    "status": "error",
                    "message": "Join room terlebih dahulu"
                }

            cursor.execute(
                "INSERT INTO room_messages(room_id, sender, message) VALUES(?, ?, ?)",
                (room_id, sender, message)
            )

            conn_db.commit()
            self.logger.info(f"Room message from {sender} to room {room_id}")

            return {
                "status": "success",
                "message": "Pesan room berhasil dikirim"
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

    def send_room_file(self, room_id, sender, filepath, filename, file_type="file"):
        if not filepath or not filename:
            return {
                "status": "error",
                "message": "File tidak valid"
            }

        if not os.path.exists(filepath):
            return {
                "status": "error",
                "message": "File tidak ditemukan di komputer pengirim"
            }

        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        try:
            cursor.execute(
                "SELECT id FROM room_members WHERE room_id=? AND username=?",
                (room_id, sender)
            )

            if not cursor.fetchone():
                return {
                    "status": "error",
                    "message": "Join room terlebih dahulu"
                }

            upload_dir = os.path.join("uploads", "rooms", str(room_id))
            os.makedirs(upload_dir, exist_ok=True)

            original_name = os.path.basename(filename)
            safe_name = original_name.replace(" ", "_")
            stored_name = f"{int(time.time() * 1000)}_{safe_name}"
            destination_path = os.path.join(upload_dir, stored_name)

            shutil.copy(filepath, destination_path)

            kind = "IMAGE" if file_type == "image" else "FILE"
            message_text = f"[{kind}] {stored_name}"

            cursor.execute(
                "INSERT INTO room_files(room_id, sender, filename, filepath, file_type) VALUES(?,?,?,?,?)",
                (room_id, sender, stored_name, destination_path, file_type)
            )

            cursor.execute(
                "INSERT INTO room_messages(room_id, sender, message) VALUES(?, ?, ?)",
                (room_id, sender, message_text)
            )

            conn_db.commit()
            self.logger.info(f"Room {file_type} from {sender} to room {room_id}: {stored_name}")

            return {
                "status": "success",
                "message": f"{kind} berhasil dikirim ke room",
                "filename": stored_name,
                "filepath": destination_path
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

    def get_room_messages(self, room_id, username):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        cursor.execute(
            "SELECT id FROM room_members WHERE room_id=? AND username=?",
            (room_id, username)
        )

        if not cursor.fetchone():
            conn_db.close()
            return {
                "status": "error",
                "message": "Anda belum join room ini",
                "messages": []
            }

        cursor.execute("""
            SELECT sender, message, created_at
            FROM room_messages
            WHERE room_id=?
            ORDER BY id ASC
        """, (room_id,))

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

    def get_room_users(self, room_id):
        conn_db = self.db.get_connection()
        cursor = conn_db.cursor()

        cursor.execute("""
            SELECT username
            FROM room_members
            WHERE room_id=?
            ORDER BY username ASC
        """, (room_id,))

        rows = cursor.fetchall()
        conn_db.close()

        users = [row[0] for row in rows]

        return {
            "status": "success",
            "users": users
        }

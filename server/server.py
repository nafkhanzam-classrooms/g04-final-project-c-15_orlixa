import socket
import threading

from shared.constants import HOST
from shared.constants import PORT

from server.protocol import recv_packet
from server.protocol import send_packet

from server.auth_manager import AuthManager
from server.logger import Logger

from server.feed_manager import FeedManager

class OrlixaServer:

    def __init__(self):

        self.auth = AuthManager()

        self.logger = Logger()

        self.feed = FeedManager()
        
        self.clients = {}

        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.server.bind(
            (HOST, PORT)
        )

        self.server.listen(100)

    def start(self):

        print(
            f"[SERVER] Running on {HOST}:{PORT}"
        )

        self.logger.info(
            "Server started"
        )

        while True:

            conn, addr = self.server.accept()

            thread = threading.Thread(
                target=self.handle_client,
                args=(conn, addr),
                daemon=True
            )

            thread.start()

    def handle_client(
        self,
        conn,
        addr
    ):

        print(
            f"[CONNECTED] {addr}"
        )

        self.logger.info(
            f"Connected {addr}"
        )

        username = None

        try:

            while True:

                packet = recv_packet(conn)

                if not packet:
                    break

                action = packet.get(
                    "action"
                )

                if action == "register":

                    response = self.auth.register(
                        packet["username"],
                        packet["password"]
                    )

                    send_packet(
                        conn,
                        response
                    )

                elif action == "login":

                    response = self.auth.login(
                        packet["username"],
                        packet["password"]
                    )

                    if response["status"] == "success":

                        username = packet["username"]

                        self.clients[
                            username
                        ] = conn

                        self.logger.info(
                            f"Login {username}"
                        )

                    send_packet(
                        conn,
                        response
                    )

                elif action == "ping":

                    send_packet(
                        conn,
                        {
                            "status": "success",
                            "message": "pong"
                        }
                    )
                elif action == "create_post":
                    
                    response = self.feed.create_post(
                        packet["username"],
                        packet["content"]
                    )

                    send_packet(
                        conn,
                        response
                    )

                elif action == "get_feed":

                    response = self.feed.get_feed()

                    send_packet(
                        conn,
                        response
                    )
                    
                elif action == "like_post":
                    
                    response = self.feed.like_post(
                        packet["post_id"],
                        packet["username"]
                    )

                    send_packet(
                        conn,
                        response
                    )

                elif action == "comment_post":

                    response = self.feed.comment_post(
                        packet["post_id"],
                        packet["username"],
                        packet["comment"]
                    )

                    send_packet(
                        conn,
                        response
                    )  
                    
                elif action == "get_comments":
                    
                    response = self.feed.get_comments(
                        packet["post_id"]
                    )

                    send_packet(
                        conn,
                        response
                    )     
                elif action == "get_like_count":
                    
                    response = self.feed.get_like_count(
                        packet["post_id"]
                    )

                    send_packet(
                        conn,
                        response
                    ) 
                elif action == "has_liked":
                    
                    response = self.feed.has_liked(
                        packet["post_id"],
                        packet["username"]
                    )

                    send_packet(
                        conn,
                        response
                    )  
                elif action == "get_online_users":
                    
                    users = list(
                        self.clients.keys()
                    )

                    send_packet(
                        conn,
                        {
                            "status": "success",
                            "users": users
                        }
                    ) 
                elif action == "send_message":
                    
                    conn_db = self.feed.db.get_connection()

                    cursor = conn_db.cursor()

                    cursor.execute(
                        """
                        INSERT INTO messages(
                            sender,
                            receiver,
                            message
                        )
                        VALUES(?,?,?)
                        """,
                        (
                            packet["sender"],
                            packet["receiver"],
                            packet["message"]
                        )
                    )

                    conn_db.commit()
                    conn_db.close()

                    send_packet(
                        conn,
                        {
                            "status":"success",
                            "message":"Pesan terkirim"
                        }
                    )

                elif action == "get_messages":

                    conn_db = self.feed.db.get_connection()

                    cursor = conn_db.cursor()

                    cursor.execute(
                        """
                        SELECT
                            sender,
                            message,
                            created_at
                        FROM messages
                        WHERE receiver=?
                        ORDER BY id DESC
                        """,
                        (
                            packet["username"],
                        )
                    )

                    rows = cursor.fetchall()

                    conn_db.close()

                    messages = []

                    for row in rows:

                        messages.append(
                            {
                                "sender":row[0],
                                "message":row[1],
                                "created_at":row[2]
                            }
                        )

                    send_packet(
                        conn,
                        {
                            "status":"success",
                            "messages":messages
                        }
                    )
                elif action == "get_conversation":
                    
                    conn_db = self.feed.db.get_connection()

                    cursor = conn_db.cursor()

                    cursor.execute(
                        """
                        SELECT
                            sender,
                            receiver,
                            message,
                            created_at
                        FROM messages
                        WHERE
                        (
                            sender=? AND receiver=?
                        )
                        OR
                        (
                            sender=? AND receiver=?
                        )
                        ORDER BY id ASC
                        """,
                        (
                            packet["user1"],
                            packet["user2"],
                            packet["user2"],
                            packet["user1"]
                        )
                    )

                    rows = cursor.fetchall()

                    conn_db.close()

                    messages = []

                    for row in rows:

                        messages.append(
                            {
                                "sender": row[0],
                                "receiver": row[1],
                                "message": row[2],
                                "created_at": row[3]
                            }
                        )

                    send_packet(
                        conn,
                        {
                            "status": "success",
                            "messages": messages
                        }
                    )
                elif action == "send_file":
                    
                    import os
                    import shutil

                    os.makedirs(
                        "uploads",
                        exist_ok=True
                    )

                    source_path = packet["filepath"]

                    filename = packet["filename"]

                    destination_path = os.path.join(
                        "uploads",
                        filename
                    )

                    shutil.copy(
                        source_path,
                        destination_path
                    )

                    conn_db = self.feed.db.get_connection()

                    cursor = conn_db.cursor()

                    cursor.execute(
                        """
                        INSERT INTO file_messages(
                            sender,
                            receiver,
                            filename,
                            filepath
                        )
                        VALUES(?,?,?,?)
                        """,
                        (
                            packet["sender"],
                            packet["receiver"],
                            filename,
                            destination_path
                        )
                    )
                    cursor.execute(
                        """
                        INSERT INTO messages(
                            sender,
                            receiver,
                            message
                        )
                        VALUES(?,?,?)
                        """,
                        (
                            packet["sender"],
                            packet["receiver"],
                            f"[FILE] {filename}"
                        )
                    )

                    conn_db.commit()
                    conn_db.close()

                    send_packet(
                        conn,
                        {
                            "status": "success",
                            "message": f"File {filename} berhasil dikirim"
                        }
                    )                                         
                else:

                    send_packet(
                        conn,
                        {
                            "status": "error",
                            "message": "Unknown action"
                        }
                    )

        except Exception as e:

            print(e)

            self.logger.error(
                str(e)
            )

        finally:

            if username:

                if username in self.clients:
                    del self.clients[
                        username
                    ]

                self.logger.info(
                    f"Logout {username}"
                )

            conn.close()

            print(
                f"[DISCONNECTED] {addr}"
            )


if __name__ == "__main__":

    server = OrlixaServer()

    server.start()
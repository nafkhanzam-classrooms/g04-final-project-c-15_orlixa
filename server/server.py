import socket
import threading

from shared.constants import HOST
from shared.constants import PORT
from server.protocol import recv_packet
from server.protocol import send_packet
from server.auth_manager import AuthManager
from server.feed_manager import FeedManager
from server.logger import Logger
from server.private_manager import PrivateManager
from server.request_router import RequestRouter
from server.room_manager import RoomManager


class OrlixaServer:
    """Server utama: fokus pada socket, koneksi client, dan delegasi request."""

    def __init__(self):
        self.logger = Logger()
        self.auth = AuthManager()
        self.feed = FeedManager()
        self.room = RoomManager(self.feed.db, self.logger)
        self.private = PrivateManager(self.feed.db, self.logger)

        self.clients = {}
        self.clients_lock = threading.Lock()

        self.router = RequestRouter(
            self.auth,
            self.feed,
            self.room,
            self.private,
            self.clients,
            self.clients_lock,
            self.logger
        )

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(100)

    def start(self):
        print(f"[SERVER] Running on {HOST}:{PORT}")
        self.logger.info("Server started")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(
                target=self.handle_client,
                args=(conn, addr),
                daemon=True
            )
            thread.start()

    def handle_client(self, conn, addr):
        print(f"[CONNECTED] {addr}")
        self.logger.info(f"Connected {addr}")
        username = None

        try:
            while True:
                packet = recv_packet(conn)

                if not packet:
                    break

                response, username = self.router.handle(
                    packet,
                    conn,
                    username
                )
                send_packet(conn, response)

        except Exception as e:
            print(e)
            self.logger.error(str(e))

        finally:
            self.remove_client(username)
            conn.close()
            print(f"[DISCONNECTED] {addr}")

    def remove_client(self, username):
        if not username:
            return

        with self.clients_lock:
            if username in self.clients:
                del self.clients[username]

        self.logger.info(f"Logout {username}")


if __name__ == "__main__":
    server = OrlixaServer()
    server.start()

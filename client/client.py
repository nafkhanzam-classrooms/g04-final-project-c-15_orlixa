import base64
import os
import socket

from shared.constants import HOST
from shared.constants import PORT
from server.protocol import send_packet
from server.protocol import recv_packet


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

    def register(self, username, password):
        send_packet(
            self.socket,
            {
                "action": "register",
                "username": username,
                "password": password
            }
        )
        return recv_packet(self.socket)

    def login(self, username, password):
        send_packet(
            self.socket,
            {
                "action": "login",
                "username": username,
                "password": password
            }
        )
        return recv_packet(self.socket)

    def ping(self):
        send_packet(
            self.socket,
            {
                "action": "ping"
            }
        )
        return recv_packet(self.socket)

    def create_post(self, username, content, image_path=None):
        packet = {
            "action": "create_post",
            "username": username,
            "content": content
        }

        if image_path:
            with open(image_path, "rb") as image_file:
                packet["image_filename"] = os.path.basename(image_path)
                packet["image_data"] = base64.b64encode(
                    image_file.read()
                ).decode("ascii")

        send_packet(self.socket, packet)
        return recv_packet(self.socket)

    def get_feed(self):
        send_packet(
            self.socket,
            {
                "action": "get_feed"
            }
        )
        return recv_packet(self.socket)

    def like_post(self, post_id, username):
        send_packet(
            self.socket,
            {
                "action": "like_post",
                "post_id": post_id,
                "username": username
            }
        )
        return recv_packet(self.socket)

    def comment_post(self, post_id, username, comment):
        send_packet(
            self.socket,
            {
                "action": "comment_post",
                "post_id": post_id,
                "username": username,
                "comment": comment
            }
        )
        return recv_packet(self.socket)

    def get_comments(self, post_id):
        send_packet(
            self.socket,
            {
                "action": "get_comments",
                "post_id": post_id
            }
        )
        return recv_packet(self.socket)

    def get_like_count(self, post_id):
        send_packet(
            self.socket,
            {
                "action": "get_like_count",
                "post_id": post_id
            }
        )
        response = recv_packet(self.socket)
        return response["count"]

    def has_liked(self, post_id, username):
        send_packet(
            self.socket,
            {
                "action": "has_liked",
                "post_id": post_id,
                "username": username
            }
        )
        return recv_packet(self.socket)

    def get_online_users(self):
        send_packet(
            self.socket,
            {
                "action": "get_online_users"
            }
        )
        return recv_packet(self.socket)

    def send_message(self, sender, receiver, message):
        send_packet(
            self.socket,
            {
                "action": "send_message",
                "sender": sender,
                "receiver": receiver,
                "message": message
            }
        )
        return recv_packet(self.socket)

    def get_messages(self, username):
        send_packet(
            self.socket,
            {
                "action": "get_messages",
                "username": username
            }
        )
        return recv_packet(self.socket)

    def get_conversation(self, user1, user2):
        send_packet(
            self.socket,
            {
                "action": "get_conversation",
                "user1": user1,
                "user2": user2
            }
        )
        return recv_packet(self.socket)

    def send_file(self, sender, receiver, filepath, filename):
        send_packet(
            self.socket,
            {
                "action": "send_file",
                "sender": sender,
                "receiver": receiver,
                "filepath": filepath,
                "filename": filename
            }
        )
        return recv_packet(self.socket)

    def create_room(self, username, room_name):
        send_packet(
            self.socket,
            {
                "action": "create_room",
                "username": username,
                "room_name": room_name
            }
        )
        return recv_packet(self.socket)

    def list_rooms(self):
        send_packet(
            self.socket,
            {
                "action": "list_rooms"
            }
        )
        return recv_packet(self.socket)

    def join_room(self, username, room_id):
        send_packet(
            self.socket,
            {
                "action": "join_room",
                "username": username,
                "room_id": room_id
            }
        )
        return recv_packet(self.socket)

    def leave_room(self, username, room_id):
        send_packet(
            self.socket,
            {
                "action": "leave_room",
                "username": username,
                "room_id": room_id
            }
        )
        return recv_packet(self.socket)

    def send_room_message(self, room_id, sender, message):
        send_packet(
            self.socket,
            {
                "action": "send_room_message",
                "room_id": room_id,
                "sender": sender,
                "message": message
            }
        )
        return recv_packet(self.socket)


    def send_room_file(self, room_id, sender, filepath, filename, file_type="file"):
        send_packet(
            self.socket,
            {
                "action": "send_room_file",
                "room_id": room_id,
                "sender": sender,
                "filepath": filepath,
                "filename": filename,
                "file_type": file_type
            }
        )
        return recv_packet(self.socket)

    def get_room_messages(self, room_id, username):
        send_packet(
            self.socket,
            {
                "action": "get_room_messages",
                "room_id": room_id,
                "username": username
            }
        )
        return recv_packet(self.socket)

    def get_room_users(self, room_id):
        send_packet(
            self.socket,
            {
                "action": "get_room_users",
                "room_id": room_id
            }
        )
        return recv_packet(self.socket)

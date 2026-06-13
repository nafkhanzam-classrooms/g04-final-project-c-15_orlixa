import socket

from shared.constants import HOST
from shared.constants import PORT

from server.protocol import send_packet
from server.protocol import recv_packet


class Client:

    def __init__(self):

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.socket.connect(
            (HOST, PORT)
        )

    def register(
        self,
        username,
        password
    ):

        send_packet(
            self.socket,
            {
                "action": "register",
                "username": username,
                "password": password
            }
        )

        return recv_packet(
            self.socket
        )

    def login(
        self,
        username,
        password
    ):

        send_packet(
            self.socket,
            {
                "action": "login",
                "username": username,
                "password": password
            }
        )

        return recv_packet(
            self.socket
        )

    def ping(self):

        send_packet(
            self.socket,
            {
                "action": "ping"
            }
        )

        return recv_packet(
            self.socket
        )
        
    def create_post(
        self,
        username,
        content
    ):

        send_packet(
            self.socket,
            {
                "action": "create_post",
                "username": username,
                "content": content
            }
        )

        return recv_packet(
            self.socket
        )              
        
    def get_feed(self):
        
        send_packet(
            self.socket,
            {
                "action": "get_feed"
            }
        )

        return recv_packet(
            self.socket
        )

    def like_post(
        self,
        post_id,
        username
    ):

        send_packet(
            self.socket,
            {
                "action":"like_post",
                "post_id":post_id,
                "username":username
            }
        )

        return recv_packet(
            self.socket
        )
        
    def comment_post(
        self,
        post_id,
        username,
        comment
    ):

        send_packet(
            self.socket,
            {
                "action":"comment_post",
                "post_id":post_id,
                "username":username,
                "comment":comment
            }
        )

        return recv_packet(
            self.socket
        )
        
    def get_comments(
        self,
        post_id
    ):

        send_packet(
            self.socket,
            {
                "action":"get_comments",
                "post_id":post_id
            }
        )

        return recv_packet(
            self.socket
        )   
        
    def get_like_count(
        self,
        post_id
    ):

        send_packet(
            self.socket,
            {
                "action":"get_like_count",
                "post_id":post_id
            }
        )

        response = recv_packet(
            self.socket
        )

        return response["count"]

    def has_liked(
        self,
        post_id,
        username
    ):

        send_packet(
            self.socket,
            {
                "action":"has_liked",
                "post_id":post_id,
                "username":username
            }
        )

        return recv_packet(
            self.socket
        )
    def get_online_users(
        self
    ):

        send_packet(
            self.socket,
            {
                "action": "get_online_users"
            }
        )

        return recv_packet(
            self.socket
        )    
    def send_message(
        self,
        sender,
        receiver,
        message
    ):

        send_packet(
            self.socket,
            {
                "action":"send_message",
                "sender":sender,
                "receiver":receiver,
                "message":message
            }
        )

        return recv_packet(
            self.socket
        )   
    def get_messages(
        self,
        username
    ):

        send_packet(
            self.socket,
            {
                "action":"get_messages",
                "username":username
            }
        )

        return recv_packet(
            self.socket
        ) 
    def get_conversation(
        self,
        user1,
        user2
    ):

        send_packet(
            self.socket,
            {
                "action": "get_conversation",
                "user1": user1,
                "user2": user2
            }
        )

        return recv_packet(
            self.socket
        )    
    def send_file(
        self,
        sender,
        receiver,
        filepath,
        filename
    ):

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

        return recv_packet(
            self.socket
        )
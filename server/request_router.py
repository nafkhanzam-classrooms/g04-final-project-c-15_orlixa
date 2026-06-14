class RequestRouter:
    """Router request server agar server.py tidak menampung logic bisnis aplikasi."""

    def __init__(self, auth, feed, room, private, clients, clients_lock, logger):
        self.auth = auth
        self.feed = feed
        self.room = room
        self.private = private
        self.clients = clients
        self.clients_lock = clients_lock
        self.logger = logger

    def handle(self, packet, conn, current_username=None):
        action = packet.get("action")

        if action == "register":
            return self.auth.register(
                packet["username"],
                packet["password"]
            ), current_username

        if action == "login":
            response = self.auth.login(
                packet["username"],
                packet["password"]
            )

            if response["status"] == "success":
                username = packet["username"]
                with self.clients_lock:
                    self.clients[username] = conn
                self.logger.info(f"Login {username}")
                return response, username

            return response, current_username

        if action == "ping":
            return {
                "status": "success",
                "message": "pong"
            }, current_username

        if action == "create_post":
            return self.feed.create_post(
                packet["username"],
                packet.get("content", ""),
                packet.get("image_filename"),
                packet.get("image_data")
            ), current_username

        if action == "get_feed":
            return self.feed.get_feed(), current_username

        if action == "like_post":
            return self.feed.like_post(
                packet["post_id"],
                packet["username"]
            ), current_username

        if action == "comment_post":
            return self.feed.comment_post(
                packet["post_id"],
                packet["username"],
                packet["comment"]
            ), current_username

        if action == "get_comments":
            return self.feed.get_comments(
                packet["post_id"]
            ), current_username

        if action == "get_like_count":
            return self.feed.get_like_count(
                packet["post_id"]
            ), current_username

        if action == "has_liked":
            return self.feed.has_liked(
                packet["post_id"],
                packet["username"]
            ), current_username

        if action == "get_online_users":
            with self.clients_lock:
                users = list(self.clients.keys())
            return {
                "status": "success",
                "users": users
            }, current_username

        if action == "create_room":
            return self.room.create_room(
                packet["username"],
                packet["room_name"]
            ), current_username

        if action == "list_rooms":
            return self.room.list_rooms(), current_username

        if action == "join_room":
            return self.room.join_room(
                packet["username"],
                packet["room_id"]
            ), current_username

        if action == "leave_room":
            return self.room.leave_room(
                packet["username"],
                packet["room_id"]
            ), current_username

        if action == "send_room_message":
            return self.room.send_room_message(
                packet["room_id"],
                packet["sender"],
                packet["message"]
            ), current_username

        if action == "send_room_file":
            return self.room.send_room_file(
                packet["room_id"],
                packet["sender"],
                packet["filepath"],
                packet["filename"],
                packet.get("file_type", "file")
            ), current_username

        if action == "get_room_messages":
            return self.room.get_room_messages(
                packet["room_id"],
                packet["username"]
            ), current_username

        if action == "get_room_users":
            return self.room.get_room_users(
                packet["room_id"]
            ), current_username

        if action == "send_message":
            return self.private.send_private_message(packet), current_username

        if action == "get_messages":
            return self.private.get_inbox_messages(
                packet["username"]
            ), current_username

        if action == "get_conversation":
            return self.private.get_conversation(
                packet["user1"],
                packet["user2"]
            ), current_username

        if action == "send_file":
            return self.private.send_private_file(packet), current_username

        return {
            "status": "error",
            "message": "Unknown action"
        }, current_username

import base64
import io
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

from PIL import Image
from PIL import ImageTk

from client.chat_window import ChatWindow
from client.room_window import RoomWindow


class FeedPage(tk.Toplevel):
    def __init__(self, parent, client, username):
        super().__init__(parent)

        self.client = client
        self.username = username

        self.title("Orlixa Feed")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.geometry("1180x760")

        self.room_map = {}
        self.selected_photo_path = None
        self.feed_image_refs = []

        self.build_ui()
        self.load_feed()
        self.load_online_users()
        self.load_rooms()
        self.auto_refresh()

    def build_ui(self):
        title = tk.Label(
            self,
            text=f"Welcome {self.username}",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        composer_frame = tk.Frame(self)
        composer_frame.pack(fill="x", padx=10)

        tk.Label(
            composer_frame,
            text="Tulis post baru",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.post_entry = tk.Text(composer_frame, height=4)
        self.post_entry.pack(fill="x")

        photo_frame = tk.Frame(composer_frame)
        photo_frame.pack(fill="x", pady=(6, 0))

        self.photo_status_label = tk.Label(
            photo_frame,
            text="Belum ada foto dipilih",
            fg="gray"
        )
        self.photo_status_label.pack(side="left")

        tk.Button(
            photo_frame,
            text="Pilih Foto",
            command=self.select_photo
        ).pack(side="left", padx=8)

        tk.Button(
            photo_frame,
            text="Hapus Foto",
            command=self.clear_selected_photo
        ).pack(side="left", padx=2)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Create Post",
            command=self.create_post
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh Feed",
            command=self.load_feed
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh Users",
            command=self.load_online_users
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh Rooms",
            command=self.load_rooms
        ).pack(side="left", padx=5)

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        user_panel = tk.Frame(main_frame, width=220, bd=1, relief="solid")
        user_panel.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(
            user_panel,
            text="ONLINE USERS",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        self.online_list = tk.Listbox(user_panel, width=25)
        self.online_list.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(
            user_panel,
            text="Open Private Chat",
            command=self.open_chat
        ).pack(fill="x", padx=5, pady=2)

        room_panel = tk.Frame(main_frame, width=240, bd=1, relief="solid")
        room_panel.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(
            room_panel,
            text="ROOM LIST",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        self.room_list = tk.Listbox(room_panel, width=30)
        self.room_list.pack(fill="both", expand=True, padx=5, pady=5)

        self.room_entry = tk.Entry(room_panel)
        self.room_entry.pack(fill="x", padx=5, pady=3)

        tk.Button(
            room_panel,
            text="Create Room",
            command=self.create_room
        ).pack(fill="x", padx=5, pady=2)

        tk.Button(
            room_panel,
            text="Join / Open Room",
            command=self.open_room
        ).pack(fill="x", padx=5, pady=2)

        tk.Button(
            room_panel,
            text="Leave Selected Room",
            command=self.leave_selected_room
        ).pack(fill="x", padx=5, pady=2)

        feed_container = tk.Frame(main_frame)
        feed_container.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(feed_container)
        self.scrollbar = ttk.Scrollbar(
            feed_container,
            orient="vertical",
            command=self.canvas.yview
        )
        self.feed_frame = tk.Frame(self.canvas)

        self.feed_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.feed_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def select_photo(self):
        filepath = filedialog.askopenfilename(
            title="Pilih foto untuk post",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("All files", "*.*")
            ]
        )

        if not filepath:
            return

        self.selected_photo_path = filepath
        filename = os.path.basename(filepath)
        self.photo_status_label.config(
            text=f"Foto dipilih: {filename}",
            fg="green"
        )

    def clear_selected_photo(self):
        self.selected_photo_path = None
        self.photo_status_label.config(
            text="Belum ada foto dipilih",
            fg="gray"
        )

    def create_post(self):
        content = self.post_entry.get("1.0", tk.END).strip()

        if not content and not self.selected_photo_path:
            messagebox.showwarning("Warning", "Isi teks atau pilih foto terlebih dahulu")
            return

        try:
            response = self.client.create_post(
                self.username,
                content,
                self.selected_photo_path
            )
        except Exception as exc:
            messagebox.showerror("Error", f"Gagal membaca/mengirim foto: {exc}")
            return

        if response["status"] == "success":
            self.post_entry.delete("1.0", tk.END)
            self.clear_selected_photo()
            self.load_feed()
        else:
            messagebox.showerror("Error", response["message"])

    def like_post(self, post_id):
        try:
            response = self.client.like_post(post_id, self.username)
            self.load_feed()
            messagebox.showinfo("Like", response["message"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def comment_post(self, post_id):
        comment = simpledialog.askstring("Comment", "Masukkan komentar:")

        if comment is None:
            return

        comment = comment.strip()

        if not comment:
            messagebox.showwarning("Warning", "Komentar tidak boleh kosong")
            return

        response = self.client.comment_post(post_id, self.username, comment)

        if response["status"] == "success":
            self.load_feed()
            messagebox.showinfo("Comment", "Komentar berhasil")
        else:
            messagebox.showerror("Error", response["message"])

    def load_online_users(self):
        try:
            response = self.client.get_online_users()
            self.online_list.delete(0, tk.END)

            for user in response["users"]:
                self.online_list.insert(tk.END, user)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_chat(self):
        selected = self.online_list.curselection()

        if not selected:
            messagebox.showwarning("Warning", "Pilih user terlebih dahulu")
            return

        target_user = self.online_list.get(selected[0])

        if target_user == self.username:
            messagebox.showwarning("Warning", "Tidak bisa chat ke diri sendiri")
            return

        ChatWindow(self, self.client, self.username, target_user)

    def create_room(self):
        room_name = self.room_entry.get().strip()

        if not room_name:
            messagebox.showwarning("Warning", "Nama room tidak boleh kosong")
            return

        response = self.client.create_room(self.username, room_name)

        if response["status"] == "success":
            self.room_entry.delete(0, tk.END)
            self.load_rooms()
            messagebox.showinfo("Room", "Room berhasil dibuat")
        else:
            messagebox.showerror("Error", response["message"])

    def load_rooms(self):
        try:
            response = self.client.list_rooms()
            self.room_list.delete(0, tk.END)
            self.room_map = {}

            for room in response.get("rooms", []):
                text = f"{room['name']} ({room['members']} user)"
                self.room_list.insert(tk.END, text)
                self.room_map[text] = room

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_room(self):
        selected = self.room_list.curselection()

        if not selected:
            messagebox.showwarning("Warning", "Pilih room terlebih dahulu")
            return

        text = self.room_list.get(selected[0])
        room = self.room_map[text]

        response = self.client.join_room(self.username, room["id"])

        if response["status"] == "success":
            RoomWindow(
                self,
                self.client,
                self.username,
                room["id"],
                room["name"]
            )
        else:
            messagebox.showerror("Error", response["message"])

    def leave_selected_room(self):
        selected = self.room_list.curselection()

        if not selected:
            messagebox.showwarning("Warning", "Pilih room terlebih dahulu")
            return

        text = self.room_list.get(selected[0])
        room = self.room_map[text]

        response = self.client.leave_room(self.username, room["id"])

        if response["status"] == "success":
            messagebox.showinfo("Room", "Berhasil keluar dari room")
            self.load_rooms()
        else:
            messagebox.showerror("Error", response["message"])

    def show_post_image(self, parent, image_data, image_filename):
        if not image_data:
            tk.Label(
                parent,
                text=f"Foto tidak dapat ditampilkan: {image_filename or '-'}",
                fg="red"
            ).pack(anchor="w", pady=5)
            return

        try:
            image_bytes = base64.b64decode(image_data.encode("ascii"))
            image = Image.open(io.BytesIO(image_bytes))
            image.thumbnail((620, 380))
            photo = ImageTk.PhotoImage(image)
            self.feed_image_refs.append(photo)

            image_label = tk.Label(parent, image=photo)
            image_label.pack(anchor="w", pady=6)
        except Exception as exc:
            tk.Label(
                parent,
                text=f"Preview foto gagal: {exc}",
                fg="red"
            ).pack(anchor="w", pady=5)

    def show_comments(self, parent, post_id):
        response = self.client.get_comments(post_id)
        comments = response.get("comments", [])

        comment_container = tk.Frame(parent, bg="#f5f5f5", padx=8, pady=6)
        comment_container.pack(fill="x", anchor="w", pady=(4, 0))

        tk.Label(
            comment_container,
            text=f"Komentar ({len(comments)})",
            font=("Arial", 9, "bold"),
            bg="#f5f5f5"
        ).pack(anchor="w")

        if not comments:
            tk.Label(
                comment_container,
                text="Belum ada komentar",
                fg="gray",
                bg="#f5f5f5"
            ).pack(anchor="w", pady=(2, 0))
            return

        for comment in comments:
            username = comment.get("username", "-")
            text = comment.get("comment", "")
            created_at = comment.get("created_at", "")

            tk.Label(
                comment_container,
                text=f"{username}: {text}",
                wraplength=620,
                justify="left",
                bg="#f5f5f5"
            ).pack(anchor="w", pady=(3, 0))

            tk.Label(
                comment_container,
                text=created_at,
                fg="gray",
                font=("Arial", 8),
                bg="#f5f5f5"
            ).pack(anchor="w")

    def load_feed(self):
        try:
            response = self.client.get_feed()

            for widget in self.feed_frame.winfo_children():
                widget.destroy()

            self.feed_image_refs = []
            posts = response.get("posts", [])

            for post in posts:
                post_frame = tk.Frame(
                    self.feed_frame,
                    bd=1,
                    relief="solid",
                    padx=10,
                    pady=10
                )
                post_frame.pack(fill="x", pady=5, anchor="w")

                tk.Label(
                    post_frame,
                    text=post["username"],
                    font=("Arial", 11, "bold")
                ).pack(anchor="w")

                content = post.get("content", "")
                if content:
                    tk.Label(
                        post_frame,
                        text=content,
                        wraplength=650,
                        justify="left"
                    ).pack(anchor="w", pady=5)

                if post.get("image_filename"):
                    self.show_post_image(
                        post_frame,
                        post.get("image_data"),
                        post.get("image_filename")
                    )

                tk.Label(
                    post_frame,
                    text=post["created_at"]
                ).pack(anchor="w")

                likes = self.client.get_like_count(post["id"])
                tk.Label(post_frame, text=f"Likes: {likes}").pack(anchor="w")

                action_frame = tk.Frame(post_frame)
                action_frame.pack(anchor="w", pady=5)

                liked = self.client.has_liked(post["id"], self.username)
                button_text = "Unlike" if liked["liked"] else "Like"

                tk.Button(
                    action_frame,
                    text=button_text,
                    command=lambda pid=post["id"]: self.like_post(pid)
                ).pack(side="left", padx=5)

                tk.Button(
                    action_frame,
                    text="Comment",
                    command=lambda pid=post["id"]: self.comment_post(pid)
                ).pack(side="left", padx=5)

                self.show_comments(post_frame, post["id"])

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def auto_refresh(self):
        try:
            self.load_feed()
            self.load_online_users()
            self.load_rooms()
        except Exception:
            pass

        self.after(3000, self.auto_refresh)

    def on_close(self):
        self.destroy()

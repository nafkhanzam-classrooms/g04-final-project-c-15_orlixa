import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

from client.chat_window import ChatWindow


class FeedPage(tk.Toplevel):

    def __init__(
        self,
        parent,
        client,
        username
    ):
        super().__init__(parent)

        self.client = client
        self.username = username

        self.title("Orlixa Feed")
        self.protocol(
        "WM_DELETE_WINDOW",
        self.on_close
        )
        self.geometry("1000x700")

        self.build_ui()

        self.load_feed()
        self.load_online_users()
        self.auto_refresh()

    def build_ui(self):

        title = tk.Label(
            self,
            text=f"Welcome {self.username}",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=10
        )

        self.post_entry = tk.Text(
            self,
            height=4
        )

        self.post_entry.pack(
            fill="x",
            padx=10
        )

        button_frame = tk.Frame(self)

        button_frame.pack(
            pady=10
        )

        tk.Button(
            button_frame,
            text="Create Post",
            command=self.create_post
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Refresh Feed",
            command=self.load_feed
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Refresh Users",
            command=self.load_online_users
        ).pack(
            side="left",
            padx=5
        )

        main_frame = tk.Frame(self)

        main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================
        # USER PANEL
        # =========================

        user_panel = tk.Frame(
            main_frame,
            width=220,
            bd=1,
            relief="solid"
        )

        user_panel.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        tk.Label(
            user_panel,
            text="ONLINE USERS",
            font=("Arial", 11, "bold")
        ).pack(
            pady=5
        )

        self.online_list = tk.Listbox(
            user_panel,
            width=25
        )

        self.online_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        tk.Button(
            user_panel,
            text="Open Chat",
            command=self.open_chat
        ).pack(
            fill="x",
            padx=5,
            pady=2
        )

        # =========================
        # FEED PANEL
        # =========================

        feed_container = tk.Frame(
            main_frame
        )

        feed_container.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            feed_container
        )

        self.scrollbar = ttk.Scrollbar(
            feed_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.feed_frame = tk.Frame(
            self.canvas
        )

        self.feed_frame.bind(
            "<Configure>",
            lambda e:
            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.feed_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

    def create_post(self):

        content = self.post_entry.get(
            "1.0",
            tk.END
        ).strip()

        if not content:
            return

        response = self.client.create_post(
            self.username,
            content
        )

        if response["status"] == "success":

            self.post_entry.delete(
                "1.0",
                tk.END
            )

            self.load_feed()

        else:

            messagebox.showerror(
                "Error",
                response["message"]
            )

    def like_post(
        self,
        post_id
    ):

        try:

            response = self.client.like_post(
                post_id,
                self.username
            )

            self.load_feed()

            messagebox.showinfo(
                "Like",
                response["message"]
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def comment_post(
        self,
        post_id
    ):

        comment = simpledialog.askstring(
            "Comment",
            "Masukkan komentar:"
        )

        if not comment:
            return

        response = self.client.comment_post(
            post_id,
            self.username,
            comment
        )

        if response["status"] == "success":

            messagebox.showinfo(
                "Comment",
                "Komentar berhasil"
            )

        else:

            messagebox.showerror(
                "Error",
                response["message"]
            )

    def load_online_users(self):

        try:

            response = self.client.get_online_users()

            self.online_list.delete(
                0,
                tk.END
            )

            for user in response["users"]:

                self.online_list.insert(
                    tk.END,
                    user
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def open_chat(self):

        selected = self.online_list.curselection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Pilih user terlebih dahulu"
            )

            return

        target_user = self.online_list.get(
            selected[0]
        )

        if target_user == self.username:

            messagebox.showwarning(
                "Warning",
                "Tidak bisa chat ke diri sendiri"
            )

            return

        ChatWindow(
            self,
            self.client,
            self.username,
            target_user
        )

    def load_feed(self):

        try:

            response = self.client.get_feed()

            for widget in self.feed_frame.winfo_children():
                widget.destroy()

            posts = response.get(
                "posts",
                []
            )

            for post in posts:

                post_frame = tk.Frame(
                    self.feed_frame,
                    bd=1,
                    relief="solid",
                    padx=10,
                    pady=10
                )

                post_frame.pack(
                    fill="x",
                    pady=5
                )

                tk.Label(
                    post_frame,
                    text=post["username"],
                    font=("Arial", 11, "bold")
                ).pack(
                    anchor="w"
                )

                tk.Label(
                    post_frame,
                    text=post["content"],
                    wraplength=650,
                    justify="left"
                ).pack(
                    anchor="w",
                    pady=5
                )

                tk.Label(
                    post_frame,
                    text=post["created_at"]
                ).pack(
                    anchor="w"
                )

                likes = self.client.get_like_count(
                    post["id"]
                )

                tk.Label(
                    post_frame,
                    text=f"❤️ {likes}"
                ).pack(
                    anchor="w"
                )

                action_frame = tk.Frame(
                    post_frame
                )

                action_frame.pack(
                    anchor="w",
                    pady=5
                )

                liked = self.client.has_liked(
                    post["id"],
                    self.username
                )

                button_text = "Like"

                if liked["liked"]:
                    button_text = "Unlike"

                tk.Button(
                    action_frame,
                    text=button_text,
                    command=lambda pid=post["id"]:
                    self.like_post(pid)
                ).pack(
                    side="left",
                    padx=5
                )

                tk.Button(
                    action_frame,
                    text="Comment",
                    command=lambda pid=post["id"]:
                    self.comment_post(pid)
                ).pack(
                    side="left",
                    padx=5
                )

        except Exception as e:

            messagebox.showerror(
                "Connection Error",
                str(e)
            )
    def auto_refresh(self):
        
        try:

            self.load_feed()

            self.load_online_users()

        except:
            pass

        self.after(
            3000,
            self.auto_refresh
        )
    def on_close(self):
        
        self.destroy()
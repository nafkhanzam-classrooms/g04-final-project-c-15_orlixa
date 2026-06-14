import tkinter as tk
from tkinter import messagebox

from client.client import Client
from client.feed_page import FeedPage


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Orlixa")
        self.geometry("450x350")
        self.resizable(False, False)

        self.client = None

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self,
            text="ORLIXA",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        username_label = tk.Label(self, text="Username")
        username_label.pack()

        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self, text="Password")
        password_label.pack()

        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(
            self,
            text="Login",
            width=20,
            command=self.login
        )
        login_button.pack(pady=10)

        register_button = tk.Button(
            self,
            text="Register",
            width=20,
            command=self.register
        )
        register_button.pack()

    def get_client(self):
        if self.client is None:
            self.client = Client()

        return self.client

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username dan password wajib diisi")
            return

        try:
            client = self.get_client()
            response = client.register(username, password)

            if response["status"] == "success":
                messagebox.showinfo("Berhasil", response["message"])
            else:
                messagebox.showerror("Gagal", response["message"])

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username dan password wajib diisi")
            return

        try:
            client = self.get_client()
            response = client.login(username, password)

            if response["status"] == "success":
                messagebox.showinfo("Login", "Login berhasil")
                feed = FeedPage(self, client, username)
                feed.focus()
            else:
                messagebox.showerror("Login Gagal", response["message"])

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

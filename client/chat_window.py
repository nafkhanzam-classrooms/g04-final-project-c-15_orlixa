import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class ChatWindow(tk.Toplevel):
    def __init__(self, parent, client, current_user, target_user):
        super().__init__(parent)

        self.client = client
        self.current_user = current_user
        self.target_user = target_user

        self.title(f"Chat with {target_user}")
        self.geometry("650x550")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.last_message_count = 0

        self.build_ui()
        self.load_messages()
        self.auto_refresh_chat()

    def build_ui(self):
        title = tk.Label(
            self,
            text=f"Chat with {self.target_user}",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)

        self.chat_box = tk.Text(self, state="disabled")
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=10)

        self.message_entry = tk.Entry(self)
        self.message_entry.pack(fill="x", padx=10, pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Send Message",
            command=self.send_message
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Send File",
            command=self.send_file
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh Chat",
            command=self.load_messages
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Open Latest File",
            command=self.open_latest_file
        ).pack(side="left", padx=5)

    def send_message(self):
        message = self.message_entry.get().strip()

        if not message:
            return

        response = self.client.send_message(
            self.current_user,
            self.target_user,
            message
        )

        if response["status"] == "success":
            self.message_entry.delete(0, tk.END)
            self.load_messages()
        else:
            messagebox.showerror("Error", response["message"])

    def load_messages(self):
        response = self.client.get_conversation(
            self.current_user,
            self.target_user
        )

        messages = response["messages"]
        current_count = len(messages)

        if self.last_message_count > 0 and current_count > self.last_message_count:
            newest = messages[-1]

            if newest["sender"] != self.current_user:
                messagebox.showinfo(
                    "Pesan Baru",
                    f"Pesan dari {newest['sender']}"
                )

        self.last_message_count = current_count

        self.chat_box.config(state="normal")
        self.chat_box.delete("1.0", tk.END)

        for msg in messages:
            prefix = "YOU" if msg["sender"] == self.current_user else msg["sender"]

            self.chat_box.insert(tk.END, f"{prefix}\n")

            message = msg["message"]
            self.chat_box.insert(tk.END, f"{message}\n")
            self.chat_box.insert(tk.END, f"{msg['created_at']}\n")
            self.chat_box.insert(tk.END, "-" * 40 + "\n")

        self.chat_box.config(state="disabled")

    def send_file(self):
        filepath = filedialog.askopenfilename()

        if not filepath:
            return

        filename = os.path.basename(filepath)

        response = self.client.send_file(
            self.current_user,
            self.target_user,
            filepath,
            filename
        )

        if response["status"] == "success":
            messagebox.showinfo(
                "File Transfer",
                f"{filename} berhasil dikirim"
            )
            self.load_messages()
        else:
            messagebox.showerror("Error", response["message"])

    def auto_refresh_chat(self):
        try:
            self.load_messages()
        except Exception:
            pass

        self.after(2000, self.auto_refresh_chat)

    def open_latest_file(self):
        response = self.client.get_conversation(
            self.current_user,
            self.target_user
        )
        messages = response["messages"]

        for msg in reversed(messages):
            text = msg["message"]

            if text.startswith("[FILE]"):
                filename = text.replace("[FILE]", "").strip()
                filepath = os.path.join("uploads", filename)

                if os.path.exists(filepath):
                    os.startfile(filepath)
                    return

                messagebox.showerror("Error", "File tidak ditemukan")
                return

        messagebox.showinfo("Info", "Belum ada file")

    def on_close(self):
        self.destroy()

import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk


class RoomWindow(tk.Toplevel):
    def __init__(self, parent, client, username, room_id, room_name):
        super().__init__(parent)

        self.client = client
        self.username = username
        self.room_id = room_id
        self.room_name = room_name

        self.title(f"Room: {room_name}")
        self.geometry("820x620")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.last_message_count = 0
        self.image_refs = []

        self.build_ui()
        self.load_messages()
        self.load_room_users()
        self.auto_refresh()

    def build_ui(self):
        title = tk.Label(
            self,
            text=f"Room: {self.room_name}",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        chat_frame = tk.Frame(main_frame)
        chat_frame.pack(side="left", fill="both", expand=True)

        user_frame = tk.Frame(main_frame, width=180, bd=1, relief="solid")
        user_frame.pack(side="right", fill="y", padx=(10, 0))

        tk.Label(
            user_frame,
            text="ROOM USERS",
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        self.user_list = tk.Listbox(user_frame, width=22)
        self.user_list.pack(fill="both", expand=True, padx=5, pady=5)

        self.chat_box = tk.Text(chat_frame, state="disabled")
        self.chat_box.pack(fill="both", expand=True)

        self.message_entry = tk.Entry(chat_frame)
        self.message_entry.pack(fill="x", pady=5)

        button_frame = tk.Frame(chat_frame)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Send",
            command=self.send_message
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Send Image",
            command=self.send_image
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Open Latest Image",
            command=self.open_latest_image
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_messages
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Leave Room",
            command=self.leave_room
        ).pack(side="left", padx=5)

    def send_message(self):
        message = self.message_entry.get().strip()

        if not message:
            return

        response = self.client.send_room_message(
            self.room_id,
            self.username,
            message
        )

        if response["status"] == "success":
            self.message_entry.delete(0, tk.END)
            self.load_messages()
        else:
            messagebox.showerror("Error", response["message"])

    def send_image(self):
        filepath = filedialog.askopenfilename(
            title="Pilih gambar",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("All files", "*.*")
            ]
        )

        if not filepath:
            return

        filename = os.path.basename(filepath)

        response = self.client.send_room_file(
            self.room_id,
            self.username,
            filepath,
            filename,
            "image"
        )

        if response["status"] == "success":
            messagebox.showinfo("Image", "Gambar berhasil dikirim ke room")
            self.load_messages()
        else:
            messagebox.showerror("Error", response["message"])

    def load_messages(self):
        response = self.client.get_room_messages(
            self.room_id,
            self.username
        )

        if response["status"] != "success":
            return

        messages = response["messages"]
        current_count = len(messages)

        if self.last_message_count > 0 and current_count > self.last_message_count:
            newest = messages[-1]

            if newest["sender"] != self.username:
                self.bell()

        self.last_message_count = current_count
        self.image_refs = []

        self.chat_box.config(state="normal")
        self.chat_box.delete("1.0", tk.END)

        for msg in messages:
            sender = "YOU" if msg["sender"] == self.username else msg["sender"]
            text = msg["message"]

            self.chat_box.insert(tk.END, f"{sender}\n")

            if text.startswith("[IMAGE]"):
                filename = text.replace("[IMAGE]", "").strip()
                image_path = os.path.join("uploads", "rooms", str(self.room_id), filename)

                self.chat_box.insert(tk.END, f"[IMAGE] {filename}\n")
                self.show_image_preview(image_path)
            else:
                self.chat_box.insert(tk.END, f"{text}\n")

            self.chat_box.insert(tk.END, f"{msg['created_at']}\n")
            self.chat_box.insert(tk.END, "-" * 40 + "\n")

        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def show_image_preview(self, image_path):
        if not os.path.exists(image_path):
            self.chat_box.insert(tk.END, "Gambar belum tersedia di folder uploads.\n")
            return

        try:
            image = Image.open(image_path)
            image.thumbnail((220, 220))
            photo = ImageTk.PhotoImage(image)
            self.image_refs.append(photo)
            self.chat_box.image_create(tk.END, image=photo)
            self.chat_box.insert(tk.END, "\n")
        except Exception as e:
            self.chat_box.insert(tk.END, f"Preview gagal: {e}\n")

    def load_room_users(self):
        response = self.client.get_room_users(self.room_id)

        if response["status"] != "success":
            return

        self.user_list.delete(0, tk.END)

        for user in response["users"]:
            self.user_list.insert(tk.END, user)

    def open_latest_image(self):
        response = self.client.get_room_messages(
            self.room_id,
            self.username
        )

        if response["status"] != "success":
            return

        for msg in reversed(response["messages"]):
            text = msg["message"]

            if text.startswith("[IMAGE]"):
                filename = text.replace("[IMAGE]", "").strip()
                image_path = os.path.join("uploads", "rooms", str(self.room_id), filename)

                if os.path.exists(image_path):
                    self.open_file(image_path)
                    return

                messagebox.showerror("Error", "File gambar tidak ditemukan")
                return

        messagebox.showinfo("Info", "Belum ada gambar di room ini")

    def open_file(self, path):
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def leave_room(self):
        response = self.client.leave_room(
            self.username,
            self.room_id
        )

        if response["status"] == "success":
            messagebox.showinfo("Room", "Berhasil keluar dari room")
            self.destroy()
        else:
            messagebox.showerror("Error", response["message"])

    def auto_refresh(self):
        try:
            self.load_messages()
            self.load_room_users()
        except Exception:
            pass

        self.after(2000, self.auto_refresh)

    def on_close(self):
        self.destroy()

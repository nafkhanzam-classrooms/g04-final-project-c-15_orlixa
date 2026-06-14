[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/90Mprfp5)
# Network Programming - Final Project [G04]

## Anggota Kelompok

| Nama | NRP | Kelas |
|--------|--------|--------|
| Rafael Wiratama | 5025241196 | C |
| Denzel Daniels | 5025241228 | C |
| Bima Novrifa Ananditya | 5025241194 | C |

---

## Link Youtube (Unlisted)

Link video demo:

```text
https://youtu.be/rz7HCvm1gGA
```

---

# Penjelasan Program

## Deskripsi

Orlixa merupakan aplikasi social media sederhana berbasis Client-Server yang dibangun menggunakan Python Socket Programming, SQLite Database, dan GUI Tkinter.

Aplikasi menggunakan protokol TCP sehingga banyak client dapat terhubung ke server secara bersamaan. Seluruh data pengguna, postingan, komentar, likes, pesan pribadi, dan file transfer disimpan secara terpusat pada server.

---

# Fitur Utama

### Authentication

- Register akun
- Login akun

### Social Feed

- Membuat postingan
- Melihat seluruh postingan
- Like / Unlike postingan
- Komentar pada postingan
- Membuat postingan foto
- Menampilkan daftar komentar langsung di bawah setiap postingan

### User Interaction

- Menampilkan user yang sedang online
- Direct Message (Private Chat)
- Riwayat percakapan

### Notification

- Notifikasi pesan baru

### File Transfer

- Mengirim file antar user
- Menyimpan file pada folder uploads
- Menampilkan file yang dikirim dalam percakapan

---

# Arsitektur Sistem

```text
+----------------+          TCP Socket          +-------------------------+
|   Client A     | <--------------------------> |                         |
| Tkinter GUI    |                              |                         |
+----------------+                              |                         |
                                                |                         |
+----------------+          TCP Socket          |      Orlixa Server      |
|   Client B     | <--------------------------> |   Multithreaded TCP     |
| Tkinter GUI    |                              |                         |
+----------------+                              |                         |
                                                |                         |
+----------------+          TCP Socket          |                         |
|   Client C     | <--------------------------> |                         |
| Tkinter GUI    |                              +-----------+-------------+
+----------------+                                          |
                                                          |
                                                          v
                                      +------------------------------------+
                                      | SQLite Database + Upload Storage   |
                                      | database/orlixa.db                 |
                                      | uploads/                           |
                                      +------------------------------------+
```

Server menangani seluruh request dari client menggunakan multithreading sehingga beberapa user dapat menggunakan aplikasi secara bersamaan.

---

# Struktur Folder

```text
FP_Progjar_Orlixa
├── client
│   ├── __init__.py
│   ├── chat_window.py
│   ├── client.py
│   ├── feed_page.py
│   ├── gui.py
│   ├── login_page.py
│   └── room_window.py
├── database
│   └── .gitkeep
├── logs
│   └── .gitkeep
├── server
│   ├── __init__.py
│   ├── auth_manager.py
│   ├── database.py
│   ├── feed_manager.py
│   ├── logger.py
│   ├── protocol.py
│   ├── private_manager.py
│   ├── request_router.py
│   ├── room_manager.py
│   └── server.py
├── shared
│   ├── __init__.py
│   └── constants.py
├── uploads
│   └── .gitkeep
├── README.md
└── requirements.txt
```

Saat program berjalan, folder tambahan dapat terbentuk otomatis:

```text
uploads
├── posts
│   └── foto_post_yang_diupload
└── rooms
    └── <room_id>
        └── gambar_room_yang_diupload
```

---

# Komponen Program

## Client

Folder:

```text
client/
```

Berfungsi untuk:

- Menampilkan GUI
- Mengirim request ke server
- Menampilkan response dari server

File utama:

## Client

| File | Fungsi |
|---|---|
| `client/gui.py` | Entry point aplikasi client. |
| `client/login_page.py` | Menampilkan halaman login dan register. |
| `client/client.py` | Mengatur komunikasi socket dari client ke server. |
| `client/feed_page.py` | Menampilkan feed, post foto, like, komentar, online user, dan daftar room. |
| `client/chat_window.py` | Menampilkan direct message dan file transfer private. |
| `client/room_window.py` | Menampilkan room chat, daftar member room, pesan room, dan gambar room. |

---

## Server

| File | Fungsi |
|---|---|
| `server/server.py` | Server utama, menerima koneksi client, membuat thread, dan melakukan routing request berdasarkan action. |
| `server/auth_manager.py` | Mengelola register dan login. |
| `server/feed_manager.py` | Mengelola post, post foto, like, komentar, dan pengambilan feed. |
| `server/room_manager.py` | Mengelola pembuatan room, join room, leave room, pesan room, user room, dan file/gambar room. |
| `server/database.py` | Membuat database, membuat tabel, dan menjalankan migrasi kolom foto pada tabel posts. |
| `server/protocol.py` | Mengatur pengiriman dan penerimaan packet JSON dengan header ukuran payload. |
| `server/logger.py` | Mencatat aktivitas server ke file log. |


Berfungsi untuk:

- Menerima koneksi client
- Menangani autentikasi
- Menangani postingan
- Menangani komentar
- Menangani likes
- Menangani direct message
- Menangani file transfer

File utama:

| File | Fungsi |
|--------|--------|
| server.py | Server utama |
| auth_manager.py | Login & Register |
| feed_manager.py | Post, Like, Comment, DM |
| database.py | SQLite Management |
| protocol.py | Packet JSON |
| logger.py | Logging Server |

---

## Shared

Folder:

```text
shared/
```

Berisi konfigurasi yang digunakan bersama oleh client dan server.

Contoh:

```python
HOST = "127.0.0.1"
PORT = 5000
HEADER_SIZE = 8
```

---

# Database

Database menggunakan SQLite.

File:

```text
database/orlixa.db
```

Tabel yang digunakan:

### users

Menyimpan data akun.

### posts

Menyimpan postingan pengguna.

### comments

Menyimpan komentar.

### likes

Menyimpan like postingan.

### follows

Disiapkan untuk fitur follow.

### messages

Menyimpan direct message.

### files

Menyimpan metadata file transfer.

---

# Cara Menjalankan Program

## Menjalankan Server

```bash
python -m server.server
```

Output:

```text
[SERVER] Running on 127.0.0.1:5000
```

---

## Menjalankan Client

```bash
python -m client.gui
```

Jalankan lebih dari satu client untuk simulasi multi-user.

---

# Skenario Pengujian

| No | Pengujian | Langkah Singkat | Hasil yang Diharapkan |
|---:|---|---|---|
| 1 | Register user | User mengisi username dan password | Akun berhasil dibuat |
| 2 | Login user | User login dengan akun valid | User masuk ke aplikasi |
| 3 | Online user list | Dua client login bersamaan | User online tampil pada daftar |
| 4 | Create post teks | User membuat post berisi teks | Post tampil di feed |
| 5 | Create post foto | User memilih foto lalu membuat post | Foto tampil di feed |
| 6 | Create post teks + foto | User mengisi teks dan memilih foto | Teks dan foto tampil pada post yang sama |
| 7 | Validasi post kosong | User membuat post tanpa teks dan foto | Sistem menolak post kosong |
| 8 | Validasi format foto | User memilih file bukan gambar | Sistem menampilkan error format tidak didukung |
| 9 | Like post | User menekan tombol Like | Jumlah like bertambah |
| 10 | Unlike post | User menekan tombol Unlike | Jumlah like berkurang |
| 11 | Comment post | User mengisi komentar | Komentar tersimpan dan tampil di bawah post |
| 12 | Komentar kosong | User mengirim komentar kosong | Sistem menolak komentar kosong |
| 13 | Create room | User membuat room baru | Room tampil pada daftar room |
| 14 | Join room | User memilih room | Jendela room terbuka |
| 15 | Send room message | User mengirim pesan room | Pesan tampil pada room chat |
| 16 | Room users | Beberapa user join room | Daftar member room tampil |
| 17 | Send image to room | User mengirim gambar di room | Gambar tampil sebagai preview room |
| 18 | Open latest image | User menekan Open Latest Image | Gambar terbaru terbuka |
| 19 | Leave room | User keluar dari room | User tidak lagi menjadi member room |
| 20 | Direct message | User mengirim pesan private | Pesan masuk ke riwayat percakapan |
| 21 | File transfer private | User mengirim file ke user lain | Metadata file tersimpan dan pesan file tampil |
| 22 | Multi client | Beberapa client aktif bersamaan | Server tetap dapat melayani banyak client |
| 23 | Server logging | Aplikasi digunakan | Aktivitas tercatat di `logs/server.log` |

---

# Screenshot Hasil

## Login Page

<img width="1637" height="877" alt="image" src="https://github.com/user-attachments/assets/14889db1-b3c1-4eb3-bd9e-e2475de83f0a" />

<img width="1643" height="932" alt="image" src="https://github.com/user-attachments/assets/3594dd59-d61b-4d5b-9beb-f188e34a45dc" />

## Feed Page

<img width="1620" height="1037" alt="image" src="https://github.com/user-attachments/assets/c0424795-c110-491d-8b84-537953aa7cba" />


## Like dan Comment

<img width="1620" height="1043" alt="image" src="https://github.com/user-attachments/assets/6cfbbc15-f126-4d99-bd1d-61bc0a701d8e" />


## Online Users

<img width="1620" height="1042" alt="image" src="https://github.com/user-attachments/assets/04e372a3-1211-489b-9f6d-3bc4810ef8e7" />


## Direct Message

<img width="1703" height="1042" alt="image" src="https://github.com/user-attachments/assets/8f79a570-001f-4c84-abc8-19bccb4f71cb" />


## Notifikasi Pesan Baru

<img width="1655" height="722" alt="Screenshot 2026-06-13 141545" src="https://github.com/user-attachments/assets/77527011-cbd1-4203-a044-1c9315e252f9" />

<img width="1637" height="735" alt="Screenshot 2026-06-13 141651" src="https://github.com/user-attachments/assets/526c151a-d1ad-4c92-8efc-d8920384cbbb" />


## File Transfer

<img width="1735" height="767" alt="Screenshot 2026-06-13 141826" src="https://github.com/user-attachments/assets/83808fe5-e18f-4d4b-bfb9-d89c0325a4cb" />
<img width="1635" height="737" alt="Screenshot 2026-06-13 141835" src="https://github.com/user-attachments/assets/364d5b4b-1f54-475a-819c-d4cd82b138d5" />
<img width="810" height="726" alt="Screenshot 2026-06-13 141859" src="https://github.com/user-attachments/assets/5dd62eee-55e4-4245-9a94-296efa2ebc47" />
<img width="1157" height="727" alt="Screenshot 2026-06-13 141938" src="https://github.com/user-attachments/assets/b1283017-0bd2-4d39-9c51-bc9c0ba99efe" />


---

# Kesimpulan

Orlixa berhasil mengimplementasikan konsep utama Pemrograman Jaringan menggunakan arsitektur Client-Server berbasis TCP Socket. Sistem mendukung banyak client secara bersamaan, penyimpanan data menggunakan SQLite, interaksi sosial berupa postingan, komentar, direct message, serta file transfer antar pengguna melalui jaringan.

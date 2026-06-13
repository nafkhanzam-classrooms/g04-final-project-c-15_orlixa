[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/90Mprfp5)
# Network Programming - Final Project [G04]

## Anggota Kelompok

| Nama | NRP | Kelas |
|--------|--------|--------|
| Rafael Wiratama | 5025241196 | C |
| Denzel Daniels | 5025241228 | C |

---

## Link Youtube (Unlisted)

Link video demo:

```text
https://youtube.com/.....
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
+-------------+
|   Client A  |
+-------------+
       |
       |
       | TCP Socket
       |
+------------------+
|     Server       |
+------------------+
       |
       |
       v
+------------------+
| SQLite Database  |
+------------------+
       ^
       |
+-------------+
|   Client B  |
+-------------+
```

Server menangani seluruh request dari client menggunakan multithreading sehingga beberapa user dapat menggunakan aplikasi secara bersamaan.

---

# Struktur Folder

```text
FP_Progjar_Orlixa
│
├── client
│   ├── __init__.py
│   ├── chat_window.py
│   ├── client.py
│   ├── feed_page.py
│   ├── gui.py
│   └── login_page.py
│
├── database
│   └── orlixa.db
│
├── logs
│   └── server.log
│
├── server
│   ├── __init__.py
│   ├── auth_manager.py
│   ├── database.py
│   ├── feed_manager.py
│   ├── logger.py
│   ├── protocol.py
│   └── server.py
│
├── shared
│   ├── __init__.py
│   └── constants.py
│
├── uploads
│   ├── image (1).jpg
│   └── file hasil transfer lainnya
│
└── requirements.txt
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

| File | Fungsi |
|--------|--------|
| client.py | Komunikasi socket client |
| login_page.py | Halaman login dan register |
| feed_page.py | Feed sosial media |
| chat_window.py | Direct Message dan File Transfer |
| gui.py | Entry point aplikasi |

---

## Server

Folder:

```text
server/
```

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

| No | Pengujian | Hasil |
|----|-----------|--------|
| 1 | Register User | Berhasil |
| 2 | Login User | Berhasil |
| 3 | Create Post | Berhasil |
| 4 | Like Post | Berhasil |
| 5 | Unlike Post | Berhasil |
| 6 | Comment Post | Berhasil |
| 7 | Online Users | Berhasil |
| 8 | Direct Message | Berhasil |
| 9 | Auto Refresh Chat | Berhasil |
| 10 | Notifikasi Pesan Baru | Berhasil |
| 11 | File Transfer | Berhasil |
| 12 | Multi Client | Berhasil |

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

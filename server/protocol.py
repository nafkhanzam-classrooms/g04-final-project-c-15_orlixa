import json
from shared.constants import HEADER_SIZE


def send_packet(conn, data):
    payload = json.dumps(data).encode()

    header = str(len(payload)).zfill(HEADER_SIZE).encode()

    conn.sendall(header)
    conn.sendall(payload)


def recv_exact(conn, size):
    data = b''

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            return None

        data += chunk

    return data


def recv_packet(conn):
    header = recv_exact(conn, HEADER_SIZE)

    if not header:
        return None

    length = int(header.decode())

    payload = recv_exact(conn, length)

    if not payload:
        return None

    return json.loads(payload.decode())
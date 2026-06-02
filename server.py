import socket

# Konfigurasi server
SERVER_IP = "0.0.0.0"
SERVER_PORT = 6727

# Membuat socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind server
server.bind((SERVER_IP, SERVER_PORT))

print("=" * 50)
print(f"UDP Server running on port {SERVER_PORT}")
print("=" * 50)

# Dictionary client
clients = {}

while True:

    # Menerima data
    data, addr = server.recvfrom(1024)

    message = data.decode()

    client_ip = addr[0]
    client_port = addr[1]

    # Register user
    if message.startswith("REGISTER:"):

        username = message.split(":")[1]

        # Simpan client
        clients[addr] = username

        print("\n" + "=" * 50)
        print("[NEW CLIENT CONNECTED]")
        print(f"Username : {username}")
        print(f"IP Address: {client_ip}")
        print(f"Port      : {client_port}")
        print("=" * 50)

        print(f"Active Clients: {len(clients)}")

        # Broadcast join notif
        for client_addr in clients:

            if client_addr != addr:

                notif = (
                    f"{username} has joined the chatroom"
                )

                server.sendto(
                    notif.encode(),
                    client_addr
                )

        continue

    # Disconnect from chatroom
    if message.startswith("LEAVE:"):

        username = clients.get(addr, "Unknown")

        print("\n" + "=" * 50)
        print("[CLIENT DISCONNECTED]")
        print(f"Username : {username}")
        print(f"IP Address: {client_ip}")
        print(f"Port      : {client_port}")
        print("=" * 50)

        # Broadcast leave notif
        for client_addr in clients:

            if client_addr != addr:

                notif = (
                    f"{username} has left the chatroom"
                )

                server.sendto(
                    notif.encode(),
                    client_addr
                )

        # Hapus client
        if addr in clients:
            del clients[addr]

        print(f"Active Clients: {len(clients)}")

        continue

    # Chat message
    username = clients.get(addr, "Unknown")

    # Hanya tampilkan pesan chat
    print(f"{username}: {message}")

    # Broadcast pesan
    for client_addr in clients:

        if client_addr != addr:

            send_message = f"{username}: {message}"

            server.sendto(
                send_message.encode(),
                client_addr
            )
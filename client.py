import socket
import threading
import sys

# Username input
USERNAME = input("Insert username: ")

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6727

# Membuat socket UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Register username ke server
register_message = f"REGISTER:{USERNAME}"

client.sendto(
    register_message.encode(),
    (SERVER_IP, SERVER_PORT)
)

import sys

# Function menerima pesan
def receive_messages():

    while True:

        try:
            data, _ = client.recvfrom(1024)

            incoming_message = data.decode()

            # Hapus input lama
            sys.stdout.write("\r")
            sys.stdout.write("\033[K")

            # Tampilkan pesan yang masuk
            print(incoming_message)

            # Tampilkan kembali pesan dengan format yang proper
            sys.stdout.write(f"<{USERNAME}>: ")
            sys.stdout.flush()

        except:
            break


# Receive
receive_thread = threading.Thread(
    target=receive_messages
)

receive_thread.daemon = True
receive_thread.start()

# Tampilan awal
print("\n" + "=" * 50)
print(f"{USERNAME} has joined the UDP chatroom")
print("Type a message and press ENTER")
print("Type 'exit' to leave the chatroom")
print("=" * 50)

# Loop chat
while True:

    message = input(f"<{USERNAME}>: ")

    # Disconnect chatroom
    if message.lower() == "exit":

        leave_message = f"LEAVE:{USERNAME}"

        client.sendto(
            leave_message.encode(),
            (SERVER_IP, SERVER_PORT)
        )

        print("\nYou left the chatroom.")

        break

    # Hapus prompt lama
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

    # Tampilkan pesan sendiri
    print(f"<{USERNAME}>(You): {message}")

    # Kirim ke server
    client.sendto(
        message.encode(),
        (SERVER_IP, SERVER_PORT)
    )

client.close()
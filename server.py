import socket
import threading
from crypto_utils import generate_keys, decrypt_message, encrypt_message

clients = []
client_keys = {}

# Server generates its RSA keys
server_private_key, server_public_key = generate_keys()

def handle_client(client_socket):
    try:
        # Step 1: Receive client's public key
        client_public_key = client_socket.recv(4096).decode()
        client_keys[client_socket] = client_public_key
        print("[+] Received client public key.")

        # Step 2: Send server's public key
        client_socket.send(server_public_key.encode())
        print("[+] Sent server public key.")

        while True:
            encrypted_msg = client_socket.recv(4096).decode()
            if not encrypted_msg:
                break

            # Step 3: Decrypt message from sender
            try:
                decrypted_msg = decrypt_message(server_private_key, encrypted_msg)
                print(f"[>] Decrypted message: {decrypted_msg}")

                # Step 4: Re-encrypt for every client
                broadcast(decrypted_msg, sender=client_socket)

            except Exception as e:
                print(f"[!] Decryption failed: {e}")
    except:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in client_keys:
            del client_keys[client_socket]
        client_socket.close()

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                peer_public_key = client_keys[client]
                encrypted = encrypt_message(peer_public_key, message)
                client.send(encrypted.encode())
            except Exception as e:
                print(f"[!] Error sending to client: {e}")
                client.close()
                if client in clients:
                    clients.remove(client)
                if client in client_keys:
                    del client_keys[client]

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("[*] Secure Server started on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connection from {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()

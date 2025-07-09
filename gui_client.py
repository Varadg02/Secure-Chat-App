import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
from crypto_utils import generate_keys, encrypt_message, decrypt_message

class SecureChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure Chat App")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        self.entry_field = tk.Entry(root, width=40)
        self.entry_field.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.private_key, self.public_key = generate_keys()
        self.server_public_key = None

        self.setup_connection()

    def setup_connection(self):
        host = simpledialog.askstring("Server IP", "Enter server IP:", parent=self.root)
        try:
            self.sock.connect((host, 9999))
        except Exception as e:
            self.display_message("⚠️ Could not connect to server.")
            return

        # Step 1: Send public key to server
        self.sock.send(self.public_key.encode())

        # Step 2: Receive server's public key
        self.server_public_key = self.sock.recv(4096).decode()

        # Start receiving messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.display_message("✅ Connected to secure server.")

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(4096).decode()
                decrypted = decrypt_message(self.private_key, data)
                self.display_message(f"🟢 Peer: {decrypted}")
            except Exception as e:
                self.display_message("❌ Connection lost or decryption failed.")
                break

    def send_message(self, event=None):
        msg = self.entry_field.get()
        if msg:
            try:
                encrypted = encrypt_message(self.server_public_key, msg)
                self.sock.send(encrypted.encode())
                self.display_message(f"🔵 You: {msg}")
                self.entry_field.delete(0, tk.END)
            except Exception as e:
                self.display_message("❌ Encryption/send failed.")

    def display_message(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureChatClient(root)
    root.mainloop()

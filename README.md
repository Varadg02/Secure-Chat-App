# 🔐 Secure Chat App (with GUI)

A simple Python-based **end-to-end encrypted chat application** using **RSA encryption**, **socket programming**, and a **Tkinter-based GUI**.

## 🧩 Features

- 💬 Real-time text messaging between two clients
- 🔐 End-to-end encryption using RSA (2048-bit)
- 🖼️ Graphical User Interface (Tkinter)
- 🔁 Message broadcasting via a local server
- 🧪 Demonstrates secure communication principles

---

## 📁 File Structure

secure_chat_app/
├── crypto_utils.py # RSA key generation and encryption/decryption
├── gui_client.py # Chat client with Tkinter GUI
└── server.py # Server to relay messages

yaml
Copy
Edit

---

## ⚙️ Requirements

- Python 3.6+
- `pycryptodome` library for RSA encryption

### 🔧 Install dependencies:

```bash
pip install pycryptodome
🚀 How to Run
1. Start the Server
bash
Copy
Edit
python server.py
This will start a socket server on localhost:9999 to relay messages between connected clients.

2. Start the Clients
Open two terminals and run the following in each:

bash
Copy
Edit
python gui_client.py
You'll be prompted to enter the server IP (e.g., 127.0.0.1 or localhost)

The clients will exchange public keys automatically.

Start typing messages to securely chat.

🔐 How It Works
Each client generates a public/private RSA key pair

Clients exchange public keys

Messages are:

Encrypted with the recipient's public key

Decrypted with the recipient's private key

Only the intended recipient can read the message.

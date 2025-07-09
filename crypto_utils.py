from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode()  # PEM format string
    public_key = key.publickey().export_key().decode()  # PEM format string
    return private_key, public_key

def encrypt_message(public_key_str, message):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_message(private_key_str, encrypted_message):
    private_key = RSA.import_key(private_key_str)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted.decode()

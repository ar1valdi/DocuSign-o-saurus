## @file main.py
# @brief GUI-based RSA key pair generator with AES-encrypted private key.
# @details This application allows users to generate RSA key pairs, encrypt the private key using a user-defined PIN and AES, and store them securely.

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


## @brief Prompt the user to choose a folder to save the private key.
# @details Method sets private_path_var variable to the selected path with private_key.pem filename.
def choose_path():
    folder = filedialog.askdirectory(title="Choose a directory for the private key")
    if folder:
        full_path = os.path.join(folder, "private_key.pem")
        private_path_var.set(full_path)


## @brief Generate SHA256 hash of a PIN.
# @param pin String input PIN
# @return Hashed bytes of the key
def hash_pin(pin: str) -> bytes:
    return hashlib.sha256(pin.encode()).digest()


## @brief Encrypts the RSA private key using AES.
# @param private_key_bytes RSA private key bytes
# @param key AES encryption key
# @return Encrypted private key bytes (IV prepended)
def encrypt_private_key(private_key_bytes: bytes, key: bytes) -> bytes:
    iv = secrets.token_bytes(16)
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(private_key_bytes) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted


## @brief Generates RSA key pair and stores them securely.
# @details The private key is encrypted using AES and the PIN provided by the user. Private key is saved in the selected directory and public in the working directory. 
def generate_keys() -> None:
    private_path = private_path_var.get()
    pin = pin_var.get()
    if not private_path:
        messagebox.showwarning("No directory selected", "Choose the directory in which the private key should be saved.")
        return
    if not pin:
        messagebox.showwarning("No PIN entered", "Enter the PIN to encrypt the private key.")
        return

    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        aes_key = hash_pin(pin)

        encrypted_private_key = encrypt_private_key(private_key_bytes, aes_key)

        with open(private_path, "wb") as priv_file:
            priv_file.write(encrypted_private_key)

        public_path = os.path.join(os.getcwd(), "public_key.pem")
        with open(public_path, "wb") as pub_file:
            pub_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        messagebox.showinfo("Success!", f"The keys have been saved correctly!\n\nPrivate: {private_path}\nPublic: {public_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error has occured:\n{e}")

if __name__ == "__main__":
    ## GUI Setup
    app = tk.Tk()
    app.title("RSA Key Generator")
    app.geometry("600x300")
    app.resizable(False, False)

    private_path_var = tk.StringVar()
    pin_var = tk.StringVar()

    # UI Elements
    label_info = tk.Label(app, text="1. Choose the private key directory", pady=10)
    label_info.pack()

    frame_path = tk.Frame(app)
    frame_path.pack(pady=5)

    entry_path = tk.Entry(frame_path, textvariable=private_path_var, width=50)
    entry_path.pack(side=tk.LEFT, padx=(10, 5))

    btn_browse = tk.Button(frame_path, text="Browse", command=choose_path)
    btn_browse.pack(side=tk.LEFT)

    label_step2 = tk.Label(app, text="2. Enter a pin to save the key", pady=10)
    label_step2.pack()

    entry_pin = ttk.Entry(app, textvariable=pin_var, show="*", width=20, justify="center", font=("Courier", 14))
    entry_pin.pack()

    label_step3 = tk.Label(app, text="2. Click, to generate keys", pady=10)
    label_step3.pack()

    btn_generate = tk.Button(app, text="Generate RSA Keys", command=generate_keys, width=25, height=2)
    btn_generate.pack()

    app.mainloop()

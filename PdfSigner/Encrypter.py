## @file Encrypter.py
# @brief Provides PDF signing, verification and AES decryption functionalities.

import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

## @brief Verifies the signature of a PDF file.
# @param pdf_path Path to the signed PDF
# @param key_path Path to the public key
# @return True if verification is successful, otherwise False
def verify(pdf_path, key_path) -> bool:
    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        with open(key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read()
            )

        pdf_content = pdf_data.split(b"\n%%__PADES__%%\n")[0]
        pdf_signature = pdf_data.split(b"\n%%__PADES__%%\n")[1]

        digest = hashlib.sha256(pdf_content).digest()

        public_key.verify(
            pdf_signature,
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False


## @brief Signs a PDF with a private key.
# @param pdf_path Path to the input PDF
# @param key_path Path to the encrypted private key
# @param pin_code PIN to decrypt the private key
# @param result_path Output directory for the signed PDF
def sign(pdf_path, key_path, pin_code, result_path):
    with open(key_path, "rb") as key_file:
        private_key_bytes = decipher_key(key_file.read(), pin_code)

    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None
    )
    digest = hashlib.sha256(pdf_content).digest()
    signature = private_key.sign(digest, padding.PKCS1v15(), hashes.SHA256())

    with open(os.path.join(result_path, 'result_signed.pdf'), "wb") as pdf_out:
        pdf_out.write(pdf_content)
        pdf_out.write(b"\n%%__PADES__%%\n")
        pdf_out.write(signature)


## @brief Decrypts AES-encrypted private key using the provided PIN.
# @param key Encrypted private key
# @param pin PIN used to generate AES key
# @return Decrypted private key bytes
def decipher_key(key: bytes, pin: str) -> bytes:
    try:
        iv = key[:16]
        ciphertext = key[16:]

        aes_key = hashlib.sha256(pin.encode()).digest()

        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend())

        decryptor = cipher.decryptor()
        plaintext_with_padding = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(128).unpadder()
        return unpadder.update(plaintext_with_padding) + unpadder.finalize()
    except ValueError as e:
        raise ValueError("Invalid PIN") from e


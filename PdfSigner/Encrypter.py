import hashlib

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def verify(pdf_path, key_path) -> bool:
    # TODO: implement ths
    return True


def sign(pdf_path, key_path, pin_code):
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=decipher_pin(pin_code),
        )

    with open(pdf_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

    # TODO: implement own signing
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(pdf_content)
    digest = hasher.finalize()

    signed_pdf = private_key.sign(digest, padding.PKCS1v15(), hashes.SHA256())

    # TODO: embed signature in pdf file

    return signed_pdf


def decipher_pin(pin):
    # TODO: implement this
    return pin


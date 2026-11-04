import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken


def _cipher(key: str) -> Fernet:
    if not key or any(bit not in "01" for bit in key):
        raise ValueError("Encryption key must be a non-empty bit string.")
    digest = hashlib.sha256(key.encode("ascii")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt(message: str, key: str) -> str:
    if not isinstance(message, str):
        raise TypeError("Message must be a string.")
    return _cipher(key).encrypt(message.encode("utf-8")).decode("ascii")


def decrypt(ciphertext: str, key: str) -> str:
    if not isinstance(ciphertext, str):
        raise TypeError("Ciphertext must be a string.")
    try:
        plaintext = _cipher(key).decrypt(ciphertext.encode("ascii"))
    except (UnicodeEncodeError, InvalidToken) as exc:
        raise ValueError(
            "Ciphertext is invalid or was encrypted with another key."
        ) from exc
    return plaintext.decode("utf-8")

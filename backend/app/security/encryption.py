import base64
import hashlib
from cryptography.fernet import Fernet


class EncryptionService:
    def __init__(self, secret_key: str):
        key = base64.urlsafe_b64encode(
            hashlib.sha256(
                secret_key.encode("utf-8")
            ).digest()
        )

        self.cipher = Fernet(key)

    def encrypt(self, value: str) -> str:
        return self.cipher.encrypt(
            value.encode("utf-8")
        ).decode("utf-8")

    def decrypt(self, value: str) -> str:
        return self.cipher.decrypt(
            value.encode("utf-8")
        ).decode("utf-8")

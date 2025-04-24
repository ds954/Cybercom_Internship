from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

class AESCipher:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        self.bs = AES.block_size

    def encrypt(self, raw):
        raw = pad(raw.encode(), self.bs)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc), self.bs).decode()
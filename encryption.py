"""Encryption logic of Bosch thermostat."""
import logging
import base64
import hashlib
import binascii
import json
from pyaes import PADDING_NONE, AESModeOfOperationECB, Decrypter, Encrypter


_LOGGER = logging.getLogger(__name__)
BS = 16

class Encryption:
    """Encryption class."""

    def __init__(self, access_key, password, magic):
        """
        Initialize encryption.

        :param str access_key: Access key to Bosch thermostat.
            If no password specified assumed as ready key to encrypt.
        :param str password: Password created with Bosch app.
        """
        key_hash = hashlib.md5(bytearray(access_key, "utf8") + magic)
        password_hash = hashlib.md5(magic + bytearray(password, "utf8"))
        self._saved_key = key_hash.hexdigest() + password_hash.hexdigest()
        self._key = binascii.unhexlify(self._saved_key)

    @property
    def key(self):
        """Return key to store in config entry."""
        return self._saved_key

    def json_encrypt(self, raw):
        try:
            if raw:
                return json.loads(self.decrypt(raw))
            return None
        except json.JSONDecodeError:
            print("ERROR decoding message")
            print(raw)

    def encrypt(self, raw):
        """Encrypt raw message."""
        if len(raw) % BS != 0:
            raw = self._pad(raw)
        cipher = Encrypter(AESModeOfOperationECB(self._key), padding=PADDING_NONE)
        ciphertext = cipher.feed(raw) + cipher.feed()
        return base64.b64encode(ciphertext)

    def decrypt(self, enc):
        """
        Decryption algorithm.

        Decrypt raw message only if length > 2.
        Padding is not working for lenght less than 2.
        """
        decrypted = "{}"
        print("Decrypting", enc)
        try:
            if enc and len(enc) > 2:
                enc = base64.b64decode(enc)
                print("Encrypted string: ", enc)
                if len(enc) % BS != 0:
                    enc = self._pad(enc)
                cipher = Decrypter(
                    AESModeOfOperationECB(self._key), padding=PADDING_NONE
                )
                decrypted = cipher.feed(enc) + cipher.feed()
                return decrypted.decode("utf8").rstrip(chr(0))
            return decrypted
        except UnicodeDecodeError as err:
            _LOGGER.error(f"Unable to decrypt: {decrypted} with error: {err}")
            print("CAN'T DECRYPT")
        except Exception as err:
            print("ERROR ENCRYPTION")

    def _pad(self, _s):
        """Pad of encryption."""
        return _s + ((BS - len(_s) % BS) * chr(0))

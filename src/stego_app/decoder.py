import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image
from typing import Any

class Decoder:
    def __init__(self, delimiter="1111111111111110"):
        self.delimiter = delimiter
        
    def _binary_to_text(self, binary_str) -> str:
        """Internal method to convert binary to text"""
        chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
        return "".join(chr(int(char, 2)) for char in chars)

    def _get_key(self, password: str) -> bytes:
        """Internal method to derive a AES key from the password."""
        password_bytes = password.encode()
        salt = b'stego_salt_123'  # Fixed salt for demonstration, in production use a random 16 bytes salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password_bytes))
        
    def decode(self, img_path: str, password: str = None) -> str:
        """Method to decode text from image
        
        Keywords arguments :
        img_path -- Path to image
        password -- Password to decrypt the message (optional)        
        """
        img = Image.open(img_path).convert("RGB")
        pixels: Any = img.load()
        
        if pixels is None:
            raise ValueError("Impossible to load image")
        
        binary_data = ""
        width, height = img.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                for channel in [r, g, b]:
                    binary_data += str(channel & 1)
                    
                    if binary_data.endswith(self.delimiter):
                        clean_bin = binary_data[:-len(self.delimiter)]
                        extracted_text = self._binary_to_text(clean_bin)

                        if password:
                            try:
                                key = self._get_key(password)
                                f = Fernet(key)
                                decrypted_msg = f.decrypt(extracted_text.encode()).decode()
                                return decrypted_msg
                            except Exception:
                                return "Error : Incorrect password or corrupted message."

                        return extracted_text
                        
        return "No text found"
                
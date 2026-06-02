import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image
from typing import Any

class Encoder:
    def __init__(self, delimiter="1111111111111110"):
        self.delimiter = delimiter
        
    def _text_to_binary(self, text: str) -> str:
        """Internal method to convert text to binary."""
        return ''.join(format(ord(char), '08b') for char in text)

    def _get_key(self, password: str, salt: str = "stego_salt_123", iterations: int = 100000) -> bytes:
        """Internal method to derive a AES key from the password."""
        password_bytes = password.encode()
        salt_bytes: bytes = salt.encode()  # Fixed salt for demonstration, in production use a random 16 bytes salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=iterations,
        )
        return base64.urlsafe_b64encode(kdf.derive(password_bytes))
        
        
    def encode(self, img_path: str, message: str, output_path: str, password: str = None, salt: str = "stego_salt_123", iterations: int = 100000) -> bool:
        """Method to inject message into image.
        
        Keywords arguments :
        img_path -- Path to the original image
        message -- Message to encode inside the image
        output_path -- Path to save the new image with encoded message
        password -- Password to encrypt the message (optional)
        salt -- Salt to use for key derivation (optional)
        iterations -- Number of iterations for key derivation (optional)
        """
        if password:
            f = Fernet(self._get_key(password, salt, iterations))
            message = f.encrypt(message.encode()).decode()

            print(f"\n[DEBUG AES] Encrypted message : {message}\n")
        
        img = Image.open(img_path).convert('RGB')
        pixels: Any = img.load()
        
        if pixels is None:
            raise ValueError("Impossible to load image")
        
        binary_msg = self._text_to_binary(message) + self.delimiter
        msg_len = len(binary_msg)
        
        width, height = img.size
        if msg_len > width * height * 3:
            raise ValueError("Err : Message is too big.")
            
        bit_idx = 0
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                channels = [r, g, b]
                
                for i in range(3):
                    if bit_idx < msg_len:
                        channels[i] = (channels[i] & ~1) | int(binary_msg[bit_idx])
                        bit_idx += 1
                        
                pixels[x, y] = tuple(channels)
                if bit_idx >= msg_len:
                    img.save(output_path)
                    print("Image encoded")
                    return True
        return False
        
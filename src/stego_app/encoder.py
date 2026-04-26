from PIL import Image

class Encoder:
    def __init__(self, delimiter="1111111111111110"):
        self.delimiter = delimiter
        
    def _text_to_binary(self, text: str) -> str:
        """Internal method to convert text to binary."""
        return ''.join(format(ord(char), '08b') for char in text)
        
    def encode(self, img_path, message, output_path) -> bool:
        """Method to inject message into image.
        
        Keywords arguments :
        img_path -- Path to the original image
        message -- Message to encode inside the image
        output_path -- Path to save the new image with encoded message
        """
        img = Image.open(img_path).convert('RGB')
        pixels = img.load()
        
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
        
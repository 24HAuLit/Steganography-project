from PIL import Image

class Decoder:
    def __init__(self, delimiter="1111111111111110"):
        self.delimiter = delimiter
        
    def _binary_to_text(self, binary_str) -> str:
        """Internal method to convert binary to text"""
        chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
        return "".join(chr(int(char, 2)) for char in chars)
        
    def decode(self, img_path):
        """Method to decode text from image
        
        Keywords arguments :
        img_path -- Path to image
        """
        img = Image.open(img_path).convert("RGB")
        pixels = img.load()
        
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
                        return self._binary_to_text(clean_bin)
                        
        return "No text found"
                
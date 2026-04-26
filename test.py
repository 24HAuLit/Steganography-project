from src.stego_app import Encoder, Decoder

def run_test():
    encoder = Encoder()
    decoder = Decoder()
    
    secret_msg = "Absolutely secret message"
    input_img = "./img/image.png"
    output_img = "./img/encoded_img.png"
    
    try:
        print("encoding...")
        encoding = encoder.encode(input_img, secret_msg, output_img)
        
        if encoding:
            print(f"Message encoded with success in {output_img}")
            
        print("decoding...")
        extracted = decoder.decode(output_img)
        
        print(f"Extracted message : {extracted}")
        
        if extracted == secret_msg:
            print("pass")
        else:
            print("failed")

    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    run_test()
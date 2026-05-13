from src.stego_app import Encoder, Decoder

def run_test():
    encoder = Encoder()
    decoder = Decoder()
    
    input_img = "./img/image.png"
    output_simple = "./img/encoded_simple.png"
    output_secure = "./img/encoded_secure.png"

    
    print("\nWithout AES")
    simple_msg = "just_a_simple_message"
    encoder.encode(input_img, simple_msg, output_simple)
    extracted_simple = decoder.decode(output_simple)
    
    print(f"Attendu : {simple_msg}")
    print(f"Extrait : {extracted_simple}")
    print("Résultat :", "PASS" if simple_msg == extracted_simple else "FAILED")

    print("\nWith AES")
    msg_secure = "confidential_message"
    password = "Ultra_mega_confidential_password"
    
    encoder.encode(input_img, msg_secure, output_secure, password=password)
    extracted_secure = decoder.decode(output_secure, password=password)
    
    print(f"Attendu : {msg_secure}")
    print(f"Extrait : {extracted_secure}")
    print("Résultat :", "PASS" if msg_secure == extracted_secure else "FAILED")


    print("\nWith wrong password")
    wrong_password = "absolutely not the right password"
    extracted_wrong = decoder.decode(output_secure, password=wrong_password)
    
    print(f"Extracted : {extracted_wrong}")
    if "Error" in extracted_wrong or "incorrect" in extracted_wrong:
        print("PASS (Access denied)")
    else:
        print("FAILED (It should have blocked access, so I did something wrong in the code)")

if __name__ == "__main__":
    run_test()
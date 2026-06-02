import streamlit as st
import os
from src.stego_app import Encoder, Decoder

st.set_page_config(page_title="AES Steganography", page_icon="🕵️", layout="centered")

st.title("🕵️ Steganography Application")
st.markdown("Hide your secret messages inside images with AES encryption.")

encoder = Encoder()
decoder = Decoder()

tab_encode, tab_decode, tab_explain = st.tabs(["🔒 Encode", "🔓 Decode", "📖 Explaination"])

with tab_encode:
    st.header("Hide a Message")
    
    encode_image = st.file_uploader("1. Upload an image (PNG mandatory)", type=['png'], key="enc_img")
    secret_message = st.text_area("2. Your secret message", placeholder="Type your text here...")
    
    st.markdown("##### 🛡️ Security (Optional)")
    encode_password = st.text_input("3. AES Encryption Password", type="password", key="enc_pwd", help="Leave blank for simple encoding without encryption.")

    with st.expander("⚙️ Advanced Options (Optional)"):
            st.markdown("Personalize the encryption key generation. **Attention: these same parameters must be used during decoding.**")
            
            col1, col2 = st.columns(2)
            with col1:
                custom_salt = st.text_input("Cryptographic Salt", value="stego_salt_123", key="enc_salt")
            with col2:
                custom_iterations = st.number_input("PBKDF2 Iterations", min_value=10000, max_value=500000, value=100000, step=10000, key="enc_iter")
    
    if st.button("Start Encoding", type="primary"):
        if encode_image and secret_message:
            with st.spinner("Processing..."):
                try:
                    input_path = "temp_input.png"
                    output_path = "temp_output.png"
                    
                    with open(input_path, "wb") as f:
                        f.write(encode_image.getbuffer())
                        
                    pwd_to_use = encode_password if encode_password else None
                    encoder.encode(
                        input_path, 
                        secret_message, 
                        output_path, 
                        password=pwd_to_use, 
                        salt=custom_salt, 
                        iterations=custom_iterations
                    )
                    
                    st.success("✅ Message hidden successfully!")
                    
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Encoded Image",
                            data=file,
                            file_name="secret_image.png",
                            mime="image/png"
                        )
                        
                    os.remove(input_path)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("⚠️ Please upload an image and write a message.")

with tab_decode:
    st.header("Reveal a Message")
    
    decode_image = st.file_uploader("1. Upload the encoded image", type=['png'], key="dec_img")
    
    st.markdown("##### 🛡️ Security")
    decode_password = st.text_input("2. Password (if the image is encrypted)", type="password", key="dec_pwd")

    with st.expander("⚙️ Advanced Options (Has to be the same as encoding)"):
            col1, col2 = st.columns(2)
            with col1:
                custom_salt_dec = st.text_input("Cryptographic Salt", value="stego_salt_123", key="dec_salt")
            with col2:
                custom_iterations_dec = st.number_input("PBKDF2 Iterations", min_value=10000, max_value=500000, value=100000, step=10000, key="dec_iter")
    
    if st.button("Start Decoding", type="primary"):
        if decode_image:
            with st.spinner("Analyzing pixels..."):
                try:
                    decode_path = "temp_decode.png"
                    with open(decode_path, "wb") as f:
                        f.write(decode_image.getbuffer())
                    
                    pwd_to_use = decode_password if decode_password else None
                    extracted_text = decoder.decode(
                        decode_path, 
                        password=pwd_to_use,
                        salt=custom_salt_dec,
                        iterations=custom_iterations_dec
                    )
                    
                    os.remove(decode_path)
                    
                    if "Error" in extracted_text or "No text found" in extracted_text:
                        st.error(extracted_text)
                    else:
                        st.success("🎉 Message revealed!")
                        st.info(extracted_text) 
                        
                except Exception as e:
                    st.error(f"Error during decoding: {e}")
        else:
            st.warning("⚠️ Please upload an image to analyze.")

with tab_explain:
    code = """
    def _get_key(self, password: str) -> bytes:
        \"""Internal method to derive a AES key from the password.\"""
        password_bytes = password.encode()  # We take our password and transform it in bytes
        salt = b'stego_salt_123'  # Fixed salt for demonstration, in production use a random 16 bytes salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # We define the algorithm we will use to encrypt
            length=32,  # The length of the key
            salt=salt,  # Salt we defined earlier
            iterations=100000,  # Number of time we will do this function
        )
        return base64.urlsafe_b64encode(kdf.derive(password_bytes))
    """

    
    st.header("📖 How does it work?")
    st.write("This project combines two fundamental cybersecurity concepts: **Steganography** (hiding the existence of the message) and **Cryptography** (making the message unreadable).")
    
    st.divider()
    
    st.subheader("1. Steganography (LSB Technique)")
    st.markdown("""
    The algorithm uses the **LSB (Least Significant Bit)** technique.
    
    * **The Concept:** A digital image is made of pixels. Each pixel contains 3 colors (Red, Green, Blue), and each color is encoded on 8 bits (a number from 0 to 255).
    * **The Trick:** If we modify only the very last bit (the 8th one) of each color, the color's value changes by a maximum of 1/255th. This difference is **completely invisible to the naked eye**.
    * **Encoding:** The application converts your text into binary (0s and 1s) and replaces the least significant bits of the image with the bits of your message.
    """)
    
    st.divider()
    
    st.subheader("2. Cryptography (AES & Fernet)")
    st.markdown("""
    To prevent a simple analysis tool from reading the hidden message, an optional security layer is added.
    
    * **Key Derivation (PBKDF2):** Your human-readable password goes through a cryptographic process (SHA-256 algorithm with 100,000 iterations). This generates an ultra-robust 256-bit cryptographic key.
    * **AES-128 Encryption:** The message is encrypted using the industry standard (AES).
    * **Authentication (HMAC):** The algorithm adds a digital signature. If even a single pixel of the encrypted image is tampered with, the system detects it and blocks the decoding, ensuring data **integrity**.

    Here you can see the part of the code derive the AES key from a password :
    """)

    st.code(code, language="python")
    
    st.divider()
    
    st.subheader("3. The Delimiter (Stop Signal)")
    st.markdown("""
    How does the program know when to stop reading? 
    A special binary sequence (`1111111111111110`) is injected at the very end of the hidden message. During decoding, the program reads the pixels one by one and stops **immediately** upon detecting this delimiter, preventing it from reading the digital "noise" in the rest of the image.
    """)
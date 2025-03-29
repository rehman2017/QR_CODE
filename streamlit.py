import streamlit as st
import qrcode
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def decode_qr_code(uploaded_file):
    image = Image.open(uploaded_file)
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(gray)
    return data if data else "No QR code detected."

st.title("QR Code Generator & Scanner")

st.sidebar.header("Options")
mode = st.sidebar.radio("Choose Mode", ["Generate QR Code", "Scan QR Code"])

if mode == "Generate QR Code":
    text = st.text_input("Enter text to generate QR Code:")
    if st.button("Generate"):
        if text:
            qr_img = generate_qr_code(text)
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            st.image(qr_img, caption="Generated QR Code")
            st.download_button("Download QR Code", buf.getvalue(), "qr_code.png", "image/png")
        else:
            st.warning("Please enter text.")

elif mode == "Scan QR Code":
    uploaded_file = st.file_uploader("Upload an image with a QR Code:", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        decoded_text = decode_qr_code(uploaded_file)
        st.success(f"Decoded Text: {decoded_text}")

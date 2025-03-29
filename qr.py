import streamlit as st
import qrcode
from PIL import Image
import cv2
import numpy as np
import io

st.set_page_config(page_title="Advanced QR Code Generator & Decoder", layout="centered")
st.markdown("<h1 style='text-align:center; color:#4CAF50;'> Advanced QR Code Generator & Decoder</h1>", unsafe_allow_html=True)
st.markdown("---")

option = st.sidebar.radio("🔘 Choose Action", ["Generate QR Code", "Decode QR Code"])

if option == "Generate QR Code":
    st.subheader("🔳 Create Your Stylish QR Code")

    data = st.text_input(" Enter Data for QR Code (text, URL, etc):")
    fg_color = st.color_picker(" Pick Foreground Color", "#000000")
    bg_color = st.color_picker(" Pick Background Color", "#ffffff")
    qr_size = st.slider(" Select QR Code Size", 100, 400, 200)

    add_logo = st.checkbox(" Add Logo in Center")
    logo_file = None
    if add_logo:
        logo_file = st.file_uploader("Upload Logo Image (PNG)", type=["png"])

    if st.button(" Generate Now"):
        if data:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGB')
            img = img.resize((qr_size, qr_size))

            # 🔗 Add Logo to Center
            if add_logo and logo_file:
                logo = Image.open(logo_file)
                logo = logo.resize((qr_size // 4, qr_size // 4))
                pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

            st.image(img, caption=" Your Stylish QR Code", use_column_width=False)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("📥 Download QR Code", buf.getvalue(), file_name="stylish_qrcode.png", mime="image/png")
        else:
            st.warning("⚠️ Please enter data to generate QR code.")

elif option == "Decode QR Code":
    st.subheader("📷 Upload QR Image to Decode")
    uploaded_file = st.file_uploader("📂 Upload QR Code (PNG, JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        st.image(image, caption=" Uploaded QR Image", use_column_width=False)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(image)

        if data:
            st.success("✅ QR Code Decoded Successfully!")
            st.code(data, language="text")
            st.button("📋 Copy Decoded Text", help="You can manually copy the text above 👆")
        else:
            st.error("❌ No data found in QR Code.")
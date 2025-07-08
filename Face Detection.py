import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

# App title and instructions
st.set_page_config(page_title="Face Detection App", layout="centered")
st.title("👤 Face Detection using Viola-Jones (Haar Cascades)")
st.markdown("""
### 📝 Instructions:
1. **Upload** a JPG or PNG image.
2. **Choose** a color for the detection rectangle.
3. **Adjust** detection sensitivity with the sliders.
4. Click **'🚀 Detect Faces'** to process the image.
5. Use the **'💾 Save Image'** button to download the result.
""")

# File uploader
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_display = img.copy()

    # Color Picker
    box_color = st.color_picker("🎨 Rectangle Color", "#00FF00")
    rgb_color = tuple(int(box_color[i:i+2], 16) for i in (1, 3, 5))  # Hex to RGB
    bgr_color = tuple(reversed(rgb_color))  # OpenCV uses BGR

    # Sliders for parameters
    scaleFactor = st.slider("🔍 scaleFactor (zoom sensitivity)", 1.1, 2.0, 1.1, 0.1)
    minNeighbors = st.slider("📐 minNeighbors (detection confidence)", 1, 10, 5)

    # Detect button
    if st.button("🚀 Detect Faces"):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

        st.success(f"✅ Detected {len(faces)} face(s)")

        for (x, y, w, h) in faces:
            # Optional: filter out non-face-like shapes (e.g., shoes)
            aspect_ratio = w / h
            if 0.75 < aspect_ratio < 1.3:  # Typical human face shape
                cv2.rectangle(img_display, (x, y), (x + w, y + h), bgr_color, 2)

        # Display result
        st.image(cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB), channels="RGB", caption="📸 Detected Faces")

        # Save and download button
        if st.button("💾 Save Image"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                save_path = tmp.name
                cv2.imwrite(save_path, img_display)
                with open(save_path, "rb") as file:
                    st.download_button("📥 Download Image", data=file, file_name="detected_faces.jpg")
            os.remove(save_path)

import sys
import os

# Add project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import streamlit as st
from blockchain import load_contract
from pyzbar.pyzbar import decode
import cv2
import numpy as np
from ai.ai_analyzer import analyze_product

st.set_page_config(page_title="Consumer Food Safety Checker", layout="centered")

st.title("🧑‍🍳 Scan Food QR & Check Safety")
st.write("Upload the QR code from the product to verify safety for your health profile.")

uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

product_id = None

if uploaded_file:
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    decoded_objs = decode(image)

    if decoded_objs:
        qr_data = decoded_objs[0].data.decode("utf-8")
        st.success(f"QR Data: {qr_data}")

        if "PRODUCT_ID" in qr_data:
            product_id = int(qr_data.split(":")[1])
        else:
            st.error("Invalid QR code format")
    else:
        st.error("Could not detect QR code. Try clearer image.")

if product_id:
    st.subheader("📦 Product Details (From Blockchain)")

    contract = load_contract()
    product = contract.functions.getProduct(product_id).call()

    _, name, ingredients, allergens, nutrition, manufacturer, timestamp = product

    st.write(f"**Name:** {name}")
    st.write(f"**Ingredients:** {ingredients}")
    st.write(f"**Allergens:** {allergens}")
    st.write(f"**Nutrition:** {nutrition}")

    st.subheader("👤 Your Health Profile")

    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    allergies = st.multiselect(
        "Select your allergies (if any)",
        ["milk", "nuts", "gluten", "soy", "seafood", "eggs"]
    )

    conditions = st.multiselect(
        "Select health conditions (if any)",
        ["diabetes", "bp", "hypertension", "cholesterol", "kidney", "heart"]
    )

    if st.button("Analyze Safety"):
        user_profile = {
            "age": age,
            "gender": gender,
            "allergies": allergies,
            "conditions": conditions
        }

        status, score, reasons = analyze_product(ingredients, allergens, nutrition, user_profile)

        st.subheader("🧪 Safety Result")
        st.markdown(f"### {status}")
        st.write(f"**Safety Score:** {score}/100")

        if reasons:
            st.write("**Reasons:**")
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.write("No major risks detected for your profile.")

import streamlit as st
from blockchain import load_contract, web3
from qr_utils import generate_qr

st.set_page_config(page_title="Manufacturer Portal", layout="centered")

st.title("🏭 Blockchain Food Product Registry")
st.write("Enter product details to store permanently on blockchain.")

name = st.text_input("Product Name")
ingredients = st.text_area("Ingredients (comma separated)")
allergens = st.text_input("Allergens")
nutrition = st.text_area("Nutrition Info")

if st.button("Store on Blockchain"):

    if name and ingredients:

        contract = load_contract()
        account = web3.eth.accounts[0]

        tx_hash = contract.functions.addProduct(
            name,
            ingredients,
            allergens,
            nutrition
        ).transact({"from": account})

        web3.eth.wait_for_transaction_receipt(tx_hash)

        product_id = contract.functions.productCount().call()

        qr_data = f"PRODUCT_ID:{product_id}"
        qr_file = generate_qr(qr_data, f"product_{product_id}.png")

        st.success(f"Product stored successfully! Product ID: {product_id}")
        st.image(qr_file, caption="Scan this QR code")

    else:
        st.error("Product name and ingredients are required.")

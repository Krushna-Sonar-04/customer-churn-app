import streamlit as st
import pickle
import numpy as np
import mysql.connector
import streamlit as st
import mysql.connector

# -------------------------------
# MySQL Connection
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sql@7154",   # 🔴 CHANGE THIS
        database="churn_db"
    )
    cursor = conn.cursor()
    st.success("✅ Connected to MySQL Database")
except Exception as e:
    st.error(f"❌ Database Connection Error: {e}")

# -------------------------------
# Load Model
# -------------------------------
model = None

try:
    with open("churn_model2.pkl", "rb") as file:
        model = pickle.load(file)
    st.success("✅ Model Loaded Successfully")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")

# -------------------------------
# Title
# -------------------------------
st.title("Customer Churn Predictor 🚀")

# -------------------------------
# Inputs
# -------------------------------
st.subheader("Enter Customer Details")

tenure = st.slider("Tenure (months)", 1, 72)
monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=100.0)

contract = st.selectbox("Contract Type", [
    "Month-to-month",
    "One year",
    "Two year"
])

# Encode contract
contract_one = 1 if contract == "One year" else 0
contract_two = 1 if contract == "Two year" else 0

# -------------------------------
# Predict Button
# -------------------------------
if st.button("Predict"):

    if model is None:
        st.error("⚠️ Model not loaded")
    else:
        try:
            # Prepare input
            input_data = np.array([[tenure, monthly_charges, contract_one, contract_two]])

            # Prediction
            prediction = model.predict(input_data)

            if prediction[0] == 1:
                result = "Churn"
                st.error("❌ Customer will churn")
                st.write("💡 Suggestion: Offer discount or long-term plan")
            else:
                result = "Stay"
                st.success("✅ Customer will stay")

            # -------------------------------
            # Save to MySQL
            # -------------------------------
            try:
                cursor.execute(
                    "INSERT INTO predictions (tenure, monthly_charges, contract_type, prediction) VALUES (%s, %s, %s, %s)",
                    (tenure, monthly_charges, contract, result)
                )
                conn.commit()
                st.success("💾 Data saved to database!")
            except Exception as db_error:
                st.error(f"❌ Database Insert Error: {db_error}")

        except Exception as e:
            st.error(f"❌ Prediction Error: {e}")
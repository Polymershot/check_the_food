import streamlit as st
import requests
import numpy as np
import pandas as pd

#  Google CLoud Run URL
FASTAPI_URL_Prediction = "https://fastapi-service-241991432743.us-west1.run.app/user_prediction/"
FASTAPI_URL_Results = "https://fastapi-service-241991432743.us-west1.run.app/results/"

#  Intro
st.title("Nutrition Prediction App")
st.markdown(
    """
    ### Welcome to the Nutrition Prediction App!
    Enter the nutritional values below to predict the food category.
    """
)

#  User Input 
with st.form(key="nutrition_form"):
    protein = st.number_input("Protein (g)", min_value=0.0001, format="%.2f")
    total_fat = st.number_input("Total Fat (g)", min_value=0.0001, format="%.2f")
    carbs = st.number_input("Carbohydrates (g)", min_value=0.0001, format="%.2f")
    total_sugars = st.number_input("Total Sugars (g)", min_value=0.0001, format="%.2f")
    total_fiber = st.number_input("Total Fiber (g)", min_value=0.0001, format="%.2f")
    calcium = st.number_input("Calcium (mg)", min_value=0.0001, format="%.2f")
    iron = st.number_input("Iron (mg)", min_value=0.0001, format="%.2f")
    sodium = st.number_input("Sodium (mg)", min_value=0.0001, format="%.2f")
    vitamin_c = st.number_input("Vitamin C (mg)", min_value=0.0001, format="%.2f")
    cholesterol = st.number_input("Cholesterol (mg)", min_value=0.0001, format="%.2f")
    saturated_fat = st.number_input("Total Saturated Fats (g)", min_value=0.0001, format="%.2f")
    vitamin_a = st.number_input("Vitamin A (IU)", min_value=0.0001, format="%.2f")

    submit_button = st.form_submit_button(label="Predict")

#  Send Data to API 
if submit_button:
    user_input = {
        "protein": np.log(protein),
        "totalFat": np.log(total_fat),
        "carbs": np.log(carbs),
        "totalSugars": np.log(total_sugars),
        "totalFiber": np.log(total_fiber),
        "calcium": np.log(calcium),
        "iron": np.log(iron),
        "sodium": np.log(sodium),
        "vitaminC": np.log(vitamin_c),
        "cholesterol": np.log(cholesterol),
        "saturatedFat": np.log(saturated_fat),
        "vitaminA": np.log(vitamin_a)
    }


    # User input is getting sent to cloud run api
    with st.spinner("Your predictions are being processed... Please wait!"):
        try:
            response = requests.post(FASTAPI_URL_Prediction, json=user_input)
        
            if response.status_code == 200:
                prediction_result = response.json()
                st.success(f"**Prediction:** {prediction_result['prediction']}")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
    
        except requests.exceptions.RequestException as e:
            st.error(f"Request Failed: {e}")


# Add option for user to get last predictions as well as input data
st.markdown("---")
st.subheader("View Past Predictions")

if st.button("Get Last 5 Predictions"):
    with st.spinner("Fetching past predictions..."):
        try:
            response = requests.get(FASTAPI_URL_Results)
            if response.status_code == 200:
                data = response.json()
                # Convert dictionary to DataFrame
                table_data = []
                for key, (input_data, prediction) in data.items():
                    input_data["Prediction"] = prediction.split(":")[1] # Extract prediction value
                    table_data.append(input_data)

                df = pd.DataFrame(table_data)
                st.table(df) # Display DataFrame as a clean table
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request Failed: {e}")

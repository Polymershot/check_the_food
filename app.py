import streamlit as st
import requests
import numpy as np

#  Google CLoud Run URL
FASTAPI_URL = "https://fastapi-service-241991432743.us-west1.run.app/user_prediction/"

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

    try:
        response = requests.post(FASTAPI_URL, json=user_input)
        
        if response.status_code == 200:
            prediction_result = response.json()
            st.success(f"**Prediction:** {prediction_result['prediction']}")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request Failed: {e}")
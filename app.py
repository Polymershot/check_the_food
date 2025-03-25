import streamlit as st
import requests
import numpy as np
import pandas as pd

#  Google CLoud Run URL
FASTAPI_URL_Prediction = "https://fastapi-service-241991432743.us-west1.run.app/user_prediction/"
FASTAPI_URL_Results = "https://fastapi-service-241991432743.us-west1.run.app/results/"

#  Intro
st.title("Nutrition Prediction App")
st.markdown("---")
st.markdown(

    """
    This web app is meant to be a prototype for the following research: 
    @misc{GroceryDB, title={Prevalence of processed foods in major US grocery stores}, 
    author={Babak Ravandi and Gordana Ispirova and Michael Sebek and Peter Mehler and Albert-László Barabási and Giulia Menichetti},
    journal={Nature Food}
    year={2025},
    dio={10.1038/s43016-024-01095-7},
    url = {https://www.nature.com/articles/s43016-024-01095-7}
    
    """
)
st.markdown("---")
st.markdown(

    """
    ### Warning!
    """
)
st.markdown(

    """
    The nutrient values should be based per 100 grams. Also, the data came pre-transformed so I did the best I could to alleviate that problem but to no avail. Most predictions will fall around a value of "3". 

    1 --> least processed 

    4--> most processed


    """
)
st.markdown("---")
st.markdown(

    """
    ### Welcome to the Nutrition Prediction App! This project is meant to be a prototype from the following
    Enter the nutritional values of your food (per 100 grams) below to predict the food category.
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
        "protein": np.sign(protein) * (np.log(1 + abs(protein))) ** 0.2,
        "totalFat": np.sign(total_fat) * (np.log(1 + abs(total_fat))) ** 0.2,
        "carbs": np.sign(carbs) * (np.log(1 + abs(carbs))) ** 0.2,
        "totalSugars": np.sign(total_sugars) * (np.log(1 + abs(total_sugars))) ** 0.2,
        "totalFiber": np.sign(total_fiber) + (np.log(1 + abs(total_fiber))) ** 0.2,
        "calcium": np.sign(calcium) * (np.log(1 + abs(calcium))) ** 0.2,
        "iron": np.sign(iron) + (np.log(1 + abs(iron))) ** 0.2,
        "sodium": np.sign(sodium) * (np.log(1 + abs(sodium))) ** 0.2,
        "vitaminC": np.sign(vitamin_c) * (np.log(1 + abs(vitamin_c))) ** 0.2,
        "cholesterol": np.sign(cholesterol) * (np.log(1 + abs(cholesterol))) ** 0.2,
        "saturatedFat": np.sign(saturated_fat) * (np.log(1 + abs(saturated_fat))) ** 0.2,
        "vitaminA": np.sign(vitamin_a) * (np.log(1 + abs(vitamin_a))) ** 0.2
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
if st.button("View Past Predictions"):
    with st.spinner("Fetching data... ⏳"):
        try:
            response = requests.get(FASTAPI_URL_Results)
        
            if response.status_code == 200:
                data = response.json()

                if data:
                    # Convert API response to a DataFrame
                    df = pd.DataFrame([
                        {**input_data, "Predicted Value": float(pred.split(":")[-1] if isinstance(pred, str) else pred)}
                        for key, (input_data, pred) in data.items()
                    ])

                    # Apply Custom Styling
                    st.dataframe(
                        df.style.set_properties(**{
                            'background-color': '#f9f9f9', 
                            'border': '1px solid #ddd', 
                            'text-align': 'center' 
                        }).set_table_styles([
                            {"selector": "th", "props": [("font-size", "16px"), ("text-align", "center")]},
                            {"selector": "td", "props": [("padding", "10px"), ("font-size", "14px")]}
                        ])
                    )

                else:
                    st.warning("No data found.")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
         
        except requests.exceptions.RequestException as e:
             st.error(f"Request Failed: {e}")

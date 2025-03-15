from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import firestore
import joblib
from google.cloud.firestore import SERVER_TIMESTAMP
import numpy as np
import os
import uvicorn

# Connect to Firestore Database
db = firestore.Client()
#print(db.collections())

# Initialize app
app = FastAPI()

# Load the ML Model
with open("rf_model.pkl", "rb") as file:
    model = joblib.load(file)

# Handle user inputs
class UserInput(BaseModel):
    protein: float
    totalFat: float
    carbs: float
    totalSugars: float
    totalFiber: float
    calcium : float
    iron: float
    sodium: float
    vitaminC: float
    cholesterol: float
    saturatedFat: float
    vitaminA: float

# Use the model to create predictions from user input
def create_prediction(user_input: UserInput) -> float:

    """
    Uses the pre-loaded model to generate a prediction from user input

    Args:
        user_input (UserInput): User input in the format of {"variable": value, ...}

    Returns:
        float: Variable type of your outcome variable
    """
    user_input = dict(user_input)
    features = np.array(list(user_input.values()))
    features = features.reshape(1,-1)
    prediction = model.predict(features)[0]
    return prediction

@app.post('/user_prediction/')
async def predict(user_input: UserInput) -> dict:

    """
    Creates and stores the user prediction into a Firestore database and makes sure it only has 5 rows at any time

    Args:
        user_input (UserInput): User input

    Returns:
        dict: Input data and predicted value
    """
    # Store prediction value
    prediction = create_prediction(user_input)
    data = dict(user_input)
    data["prediction"] = prediction
    data["timestamp"] = SERVER_TIMESTAMP
    db_ref = db.collection("predictions").add(data)

    # Limit database size
    recent_rows = db.collection("predictions").order_by("timestamp").get()
    if len(recent_rows) > 5:
        oldest_row = recent_rows[0]
        db.collection("predictions").document(oldest_row.id).delete()

    return {"input": user_input, "prediction": prediction}

@app.get("/results/")
async def get_results() -> dict:

    """
    Output the last 5 predictions as well as the corresponding input data

    Returns:
        dict: a dictionary of the input values and predicted values in descending order of time created
    """
    recent_rows = db.collection("predictions").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    results = {}
    for i, row in enumerate(recent_rows):
        row_dict = row.to_dict()
        input_data = {key: value for key, value in row_dict.items() if key not in ["prediction", "timestamp"]}
        results[f"Prediction {i+1}"] = (input_data, "Predicted Value:" + str(row_dict["prediction"]))
    return results

@app.get("/")
def read_root():
    return {"message": "Fast API is working"}

if __name__ == "__main__":
    port = os.getenv("PORT", "8080")
    uvicorn.run(app, host="0.0.0.0", port=port)

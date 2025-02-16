import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


st.title("Student Performance Predictor")
st.markdown("This app predicts student performance based on input features.")

# Input fields for user data
gender = st.selectbox("Gender", options=["male", "female"])
ethnicity = st.selectbox("Race/Ethnicity", options=["group A", "group B", "group C", "group D", "group E"])
parental_level_of_education = st.selectbox("Parental Level of Education", options=[
    "some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"])
lunch = st.selectbox("Lunch", options=["standard", "free/reduced"])
test_preparation_course = st.selectbox("Test Preparation Course", options=["none", "completed"])
reading_score = st.number_input("Reading Score", min_value=0, max_value=100, step=1)
writing_score = st.number_input("Writing Score", min_value=0, max_value=100, step=1)

if st.button("Predict"):
    # Creating data object
    data = CustomData(
        gender=gender,
        race_ethnicity=ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=reading_score,
        writing_score=writing_score
    )
    pred_df = data.get_data_as_data_frame()

    # Make predictions
    try:
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        st.success(f"Predicted Maths Score: {round(results[0])}")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("\n"*10)
st.write("---")
st.write("**Project by:** [🔗](https://github.com/pranavharke/Student_Performance_Indicator) Pranav Harke")

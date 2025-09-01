# MLPayGrade Hugging Face Spaces Deployment
# This file will be automatically deployed on Hugging Face Spaces

import gradio as gr
import joblib
import json
import pickle
import pandas as pd
import numpy as np
import os

# Load model components
def load_model():
    """Load all saved model components"""
    try:
        # Load model and scaler
        model = joblib.load('best_model.pkl')
        scaler = joblib.load('scaler.pkl')

        # Load feature names
        with open('feature_names.json', 'r') as f:
            feature_names = json.load(f)

        # Load deployment functions
        with open('deployment_functions.pkl', 'rb') as f:
            deployment_data = pickle.load(f)

        return model, scaler, feature_names, deployment_data
    except Exception as e:
        print(f"Error loading model components: {e}")
        return None, None, None, None

def engineer_features_simple(job_title, experience_level, company_size, employment_type, company_location, remote_ratio):
    """Simple feature engineering without complex dependencies"""

    # Basic mappings
    exp_mapping = {"EN": 1, "MI": 2, "SE": 3, "EX": 4}
    size_mapping = {"S": 1, "M": 2, "L": 3}
    emp_mapping = {"FT": 1, "PT": 0.5, "CT": 0.8, "FL": 0.7}

    # Create features
    features = {}

    # Update with feature engineering
    features['work_year'] = 2024 # Current year
    features['remote_ratio'] = remote_ratio
    features['experience_level'] = exp_mapping.get(experience_level, 0)
    features['company_size'] = size_mapping.get(company_size, 0)
    features['employment_type'] = emp_mapping.get(employment_type, 0)

    # One-hot encoding for job title and company location
    # Ensure deployment_data is loaded before accessing it
    model, scaler, feature_names, deployment_data = load_model() # Reloading to ensure deployment_data is available

    if deployment_data and 'feature_names' in deployment_data:
        # Extract one-hot encoded columns from feature_names
        # Use the first 5 job title categories from the training data as options
        jt_category_cols = [col for col in deployment_data['feature_names'] if col.startswith('job_title_category_')]
        # Extract the category name from the column name
        jt_category_names = [col.replace('job_title_category_', '') for col in jt_category_cols]

        cl_cols = [col for col in deployment_data['feature_names'] if col.startswith('country_')]
        # Extract the country name from the column name
        cl_names = [col.replace('country_', '') for col in cl_cols]


        # One-hot encode job title
        if job_title:
            # Check if the selected job title is one of the categorized roles
            if job_title in jt_category_names:
                 jt_key = 'job_title_category_' + job_title
                 if jt_key in deployment_data['feature_names']:
                     features[jt_key] = 1
            else:
                 # If not one of the categories, it's 'Other_Roles'
                 jt_key = 'job_title_category_Other_Roles'
                 if jt_key in deployment_data['feature_names']:
                     features[jt_key] = 1

        # One-hot encode company location
        if company_location:
            cl_key = 'country_' + company_location.replace(" ", "_").replace("/", "_")
            if cl_key in deployment_data['feature_names']:
                features[cl_key] = 1
            # Handle 'Other_Countries' if the location is not in the training data
            else:
                cl_key = 'country_Other_Countries'
                if cl_key in deployment_data['feature_names']:
                    features[cl_key] = 1


    # Pad features with zeros for missing one-hot encoded features
    if deployment_data and 'feature_names' in deployment_data:
        for col in deployment_data['feature_names']:
            if col not in features:
                features[col] = 0

    # Ensure all feature names from training are present, even if 0
    full_features = {name: features.get(name, 0) for name in deployment_data['feature_names']}

    return full_features


# The main prediction function
def predict_salary(job_title, experience_level, company_size, employment_type, company_location, remote_ratio):
    try:
        # Get model components
        model, scaler, feature_names, deployment_data = load_model()

        # Check if components loaded
        if model is None or scaler is None or feature_names is None or deployment_data is None:
            return "Error: Model components could not be loaded."

        # Engineer features
        input_features = engineer_features_simple(job_title, experience_level, company_size, employment_type, company_location, remote_ratio)

        # Create DataFrame
        df = pd.DataFrame([input_features])
        # Ensure correct order of features based on the training data
        df = df[feature_names]

        # Scale features
        scaled_features = scaler.transform(df)

        # Make prediction
        predicted_salary = model.predict(scaled_features)[0]

        # Return a range and confidence score
        # These are example values, you might want to derive them based on model performance or prediction uncertainty
        margin_of_error = predicted_salary * 0.15 # Example 15% margin
        salary_min = int(predicted_salary - margin_of_error)
        salary_max = int(predicted_salary + margin_of_error)

        result_range = f"Estimated Salary Range: ${salary_min:,} - ${salary_max:,}"

        return result_range


    except Exception as e:
        print(f"Prediction Error: {e}")
        return "An error occurred during prediction. Please check inputs."

# Pre-defined choices for dropdowns - Limiting to 5 core ML/AI roles + 'Other_Roles'
# These should align with the job_title_category feature engineering
JOB_TITLE_CATEGORIES = ["Data_Scientist", "ML_Engineer", "AI_Engineer", "Data_Engineer", "Data_Analyst", "Other_Roles"]

# Pre-defined choices for locations - Using the extracted country names from feature_names
# Load feature names to get the list of countries
_, _, feature_names, _ = load_model()
if feature_names:
     LOCATIONS = [col.replace('country_', '') for col in feature_names if col.startswith('country_')]
     # Filter out 'Other_Countries' if you don't want it as an explicit option
     LOCATIONS = [loc for loc in LOCATIONS if loc != 'Other_Countries']
else:
     LOCATIONS = ["USA", "United Kingdom", "Canada", "Germany", "France", "Spain", "India", "Australia", "Japan"] # Fallback

# Custom CSS for font styling
CUSTOM_CSS = """
:root {
  --font-family: 'Times New Roman', Times, serif;
}
body {
  font-family: var(--font-family);
}
"""

# The Gradio app interface
with gr.Blocks(theme=gr.themes.Soft(), css=CUSTOM_CSS) as demo:
    gr.Markdown("# Title - Machine Learning Salary Predictor")
    gr.Markdown("Looking for your next role? Use our salary predictor to get a glimpse into which roles are paying the most depending on various factors.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📋 Job Details")

            # Use the limited job title categories
            job_title = gr.Dropdown(
                choices=JOB_TITLE_CATEGORIES,
                label="Job Title Category",
                info="Select the general job category",
                allow_custom_value=False
            )

            experience_level = gr.Radio(
                choices=["EN", "MI", "SE", "EX"],
                label="Experience Level",
                info="EN (Entry-level), MI (Mid-level), SE (Senior), EX (Executive)",
                type="value"
            )

            company_location = gr.Dropdown(
                choices=LOCATIONS,
                label="Company Location",
                info="Select the company's country",
                allow_custom_value=False
            )

            company_size = gr.Radio(
                choices=["S", "M", "L"],
                label="Company Size",
                info="S (<50), M (50-250), L (>250)"
            )

            employment_type = gr.Radio(
                choices=["FT", "PT", "CT", "FL"],
                label="Employment Type",
                info="FT (Full-Time), PT (Part-Time), CT (Contract), FL (Freelance)"
            )

            remote_ratio = gr.Radio(
                choices=[0, 50, 100],
                label="Remote Work",
                info="0% (On-site), 50% (Hybrid), 100% (Fully Remote)"
            )

            predict_btn = gr.Button("Predict")

        with gr.Column(scale=2):
            gr.Markdown("## 📈 Prediction Results")

            with gr.Row():
                salary_output = gr.Textbox(
                    label="Estimated Annual Salary Range",
                    value="Enter job details and click Predict",
                    scale=2
                )

            gr.Markdown("## 🎯 What-If Analysis")
            gr.Markdown("Try changing the parameters above to see how they affect salary predictions!")

    # Event handlers
    predict_btn.click(
        fn=predict_salary,
        inputs=[job_title, experience_level, company_size, employment_type, company_location, remote_ratio],
        outputs=[salary_output]
    )

    gr.Markdown("---")
    gr.Markdown("""
    <div style="text-align: center; color: #6c757d;">
        <h4>MLPayGrade Advanced Track - Deployed on Hugging Face Spaces</h4>
    </div>
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()

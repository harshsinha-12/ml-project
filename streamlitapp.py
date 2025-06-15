import streamlit as st
import pandas as pd
import numpy as np
import os
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Set page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="📚",
    layout="wide"
)

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4527A0;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5E35B1;
        margin-top: 0;
    }
    .prediction-box {
        background-color: #E8EAF6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .prediction-value {
        font-size: 3rem;
        font-weight: 700;
        color: #3949AB;
    }
    .feature-text {
        font-size: 1rem;
        color: #555;
    }
    .stButton>button {
        background-color: #5E35B1;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 30px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #4527A0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<p class="main-header">Student Performance Predictor</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Predict math scores based on student attributes</p>', unsafe_allow_html=True)
    with col2:
        st.image("https://img.icons8.com/color/96/000000/student-male--v1.png", width=100)
    
    st.markdown("---")
    
    # Sidebar for inputs
    st.sidebar.header("Student Information")
    
    with st.sidebar.form("prediction_form"):
        # Student information inputs
        gender = st.selectbox("Gender", ["male", "female"])
        
        race_ethnicity = st.selectbox(
            "Race/Ethnicity",
            ["group A", "group B", "group C", "group D", "group E"]
        )
        
        parental_level_of_education = st.selectbox(
            "Parental Level of Education",
            [
                "some high school",
                "high school",
                "some college",
                "associate's degree",
                "bachelor's degree",
                "master's degree"
            ]
        )
        
        lunch = st.selectbox("Lunch Type", ["standard", "free/reduced"])
        
        test_preparation_course = st.selectbox(
            "Test Preparation Course",
            ["none", "completed"]
        )
        
        # Create two columns for reading and writing scores
        col1, col2 = st.columns(2)
        with col1:
            reading_score = st.slider("Reading Score", 0, 100, 50)
        with col2:
            writing_score = st.slider("Writing Score", 0, 100, 50)
            
        submit_button = st.form_submit_button(label="Predict Math Score")
    
    # Main content
    tab1, tab2 = st.tabs(["Prediction", "About the Model"])
    
    with tab1:
        if submit_button:
            # Create CustomData instance
            data = CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score
            )
            
            # Get data as DataFrame
            df = data.get_data_as_data_frame()
            
            # Display user inputs
            st.subheader("Student Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Gender:** {gender}")
                st.markdown(f"**Race/Ethnicity:** {race_ethnicity}")
                st.markdown(f"**Parental Education:** {parental_level_of_education}")
            with col2:
                st.markdown(f"**Lunch Type:** {lunch}")
                st.markdown(f"**Test Preparation:** {test_preparation_course}")
                st.markdown(f"**Reading Score:** {reading_score}")
                st.markdown(f"**Writing Score:** {writing_score}")
            
            try:
                # Make prediction
                st.markdown("---")
                with st.spinner("Calculating prediction..."):
                    predict_pipeline = PredictPipeline()
                    prediction = predict_pipeline.predict(df)
                
                # Display prediction
                st.success("Prediction complete!")
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.markdown('<p>Predicted Math Score</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="prediction-value">{prediction[0]:.2f}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Additional visualization - gauge chart for the prediction
                import plotly.graph_objects as go
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prediction[0],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Math Score", 'font': {'size': 24}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "#5E35B1"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 50], 'color': '#FFCDD2'},
                            {'range': [50, 75], 'color': '#FFECB3'},
                            {'range': [75, 100], 'color': '#C8E6C9'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': prediction[0]
                        }
                    }
                ))
                
                st.plotly_chart(fig)
                
            except Exception as e:
                st.error(f"An error occurred during prediction: {str(e)}")
        else:
            st.info("👈 Enter student information in the sidebar and click 'Predict Math Score'")
            
            # Sample prediction visualization
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("https://img.icons8.com/color/240/000000/math.png", width=150)
                st.markdown('<p style="text-align: center; font-size: 1.2rem;">Fill in the student details to predict their math score</p>', unsafe_allow_html=True)
    
    with tab2:
        st.header("About the Student Performance Prediction Model")
        
        st.markdown("""
        This application uses a machine learning model to predict a student's math score based on various attributes:
        
        - **Gender**: Male or Female
        - **Race/Ethnicity**: Group A through E
        - **Parental Level of Education**: From some high school to master's degree
        - **Lunch Type**: Standard or Free/Reduced
        - **Test Preparation Course**: Completed or None
        - **Reading Score**: Score in reading test (0-100)
        - **Writing Score**: Score in writing test (0-100)
        
        ### Model Details
        
        The prediction model is trained on a dataset of student performance metrics. The machine learning pipeline includes:
        
        1. **Data Preprocessing**: Handling categorical variables and scaling numerical features
        2. **Model Training**: Using various regression algorithms
        3. **Model Selection**: Selecting the best performing model based on evaluation metrics
        
        ### Interpretation
        
        The predicted score is an estimate of how a student with the given attributes might perform on a math test.
        Scores range from 0 to 100, with higher scores indicating better performance.
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### How to Use This Tool
        
        1. Enter the student's information in the sidebar
        2. Click "Predict Math Score"
        3. View the predicted math score and visualization
        
        This tool can be useful for educators to identify students who might need additional support
        or for parents to understand factors that might affect their child's academic performance.
        """)

if __name__ == "__main__":
    main()

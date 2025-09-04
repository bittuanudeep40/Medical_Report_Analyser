# app.py (Final Streamlit Version)
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agent import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="MediVerse AI",
    page_icon="⚕️",
    layout="centered"
)

# --- UI Elements ---
st.title("⚕️ MediVerse AI")
st.markdown("Welcome to the future of health analysis. Upload a medical report to get clear insights and potential risk factors in seconds.")

# File uploader widget
uploaded_file = st.file_uploader("Drag & drop or click to upload your medical report", type=["txt"])

# --- Main Logic ---
if uploaded_file is not None:
    # Read the content of the uploaded file
    medical_report = uploaded_file.read().decode("utf-8")
    
    st.info("Analyzing the medical report... This may take a moment.")

    with st.spinner('Running diagnostics with AI specialists...'):
        # Run individual specialists concurrently
        agents = {
            "Cardiologist": Cardiologist(medical_report),
            "Psychologist": Psychologist(medical_report),
            "Pulmonologist": Pulmonologist(medical_report)
        }

        responses = {}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(agent.run): name for name, agent in agents.items()}
            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    responses[agent_name] = future.result()
                except Exception as e:
                    st.error(f"An error occurred with the {agent_name} agent: {e}")
                    # Stop execution if an agent fails
                    st.stop()

        # Run multidisciplinary agent
        team_agent = MultidisciplinaryTeam(
            cardiologist_report=responses.get("Cardiologist", ""),
            psychologist_report=responses.get("Psychologist", ""),
            pulmonologist_report=responses.get("Pulmonologist", "")
        )
        final_diagnosis = team_agent.run()

    # Display the final diagnosis
    st.success("Analysis Complete!")
    st.subheader("Final Diagnosis")
    st.markdown(final_diagnosis)

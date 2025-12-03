import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
st.set_page_config(page_title="Multi-AI Agent", layout="centered")
st.title("Multi-AI Agent")

system_prompt = st.text_area("Define the system prompt", value="You are a helpful AI assistant.", height=100)
select_model = st.selectbox("Select AI Model", options=settings.allowed_model_names)
allow_external_search = st.checkbox("Allow Web Search", value=False)
query_input = st.text_area("Enter your query:", height=150)

BACKEND_API_URL = "http://localhost:9999/chat"

if st.button("Ask Agent") and query_input.strip():
    try:
        payload = {
            "model_name": select_model,
            "query": [query_input],
            "allow_search": allow_external_search,
            "system_prompt": system_prompt
        }
        logger.info(f"Sending request to backend API with model: {select_model}")
        response = requests.post(BACKEND_API_URL, json=payload)
        response.raise_for_status()
        if response.status_code == 200:           
            data = response.json().get("response", {})
            st.subheader("AI Response:")
            st.markdown(data.replace("\n", "<br>"), unsafe_allow_html=True)

        else:
            logger.error(f"Backend API returned error status: {response.status_code}")
            st.error(f"Error from AI service: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to backend API failed: {e}")
        st.error(f"An error occurred while contacting the AI service: {e}")
    except CustomException as ce:
        logger.error(f"Custom exception occurred: {ce.message}")
        st.error(f"An error occurred: {ce.message}")



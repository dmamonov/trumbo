import os
import logging

import streamlit as st
from dotenv import load_dotenv
from streamlit_theme import st_theme

from components.instruction import component as instruction_component
from components.knowledge import component as knowledge_component
from components.chat import component as chat_component

# Load environment variables
load_dotenv(".env.local")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(handler)

def initialize_session_state() -> None:
    """Initialize the session state variables if they are not already set."""
    env_vars = {
        "MISTRAL_API_KEY": "MISTRAL_API_KEY",
        "MISTRAL_MODEL_NAME": "MISTRAL_MODEL_NAME",
        "SCRIPT_TEXT": "SCRIPT_TEXT",
    }
    for var, env in env_vars.items():
        if var not in st.session_state:
            value = os.getenv(env)
            if value is None:
                message = "Missing env variable: " + env
                logger.exception(message)
                # raise ValueError(message)
            st.session_state[var] = value

# Set the page layout to wide
st.set_page_config(
    page_title="Snippets",
    page_icon="🔥",
    layout="wide",
)

# Initialize the session state variables
initialize_session_state()

# Main Streamlit app starts here
instruction_component()
knowledge_component()
chat_component()

# Custom CSS
css = """
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)
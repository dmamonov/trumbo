import logging
import os
from textwrap import dedent

import dotenv
from langchain.schema import AIMessage
from mistralai import Mistral

import streamlit as st

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(handler)

dotenv.load_dotenv(".env.local")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MISTRAL_MODEL_NAME = os.environ["MISTRAL_MODEL_NAME"]

RAG_PROMPT_TEMPLATE = dedent("""
    Reply to the user based on the script using markdown.
    If the context does not contain enough information to answer the question, say "I don't know".
    Question: {question}
""".strip())


def generate_response(messages) -> AIMessage:
    """Generate a response using the OpenAI API."""
    logger.debug(f"Generating response with messages: {messages}")
    mistral_client = Mistral(api_key=MISTRAL_API_KEY)
    chat_response = mistral_client.chat.complete(
        model = MISTRAL_MODEL_NAME,
        messages = messages,
        temperature = 0,
    )
    return chat_response.choices[0].message

def component() -> None:
    """Main component for the tab."""

    st.header("Chat with your script")

    # Display chat messages from history on app rerun
    if "messages" in st.session_state:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] != "system":
                    st.markdown(message["content"])

    # Accept user input
    if st.session_state.get("SCRIPT_TEXT") is None or st.session_state["SCRIPT_TEXT"] == "":
        st.warning("Please load a script in the Knowledge tab.")
        return

    if prompt := st.chat_input("Say something..."):
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "system",
                "content": dedent(
                    f"""
                    You are a helpful assistant for scriptwriters and script editors.
                    Your task is to answer the user's questions based on the script provided.
                    Script: {st.session_state['SCRIPT_TEXT']}
                    """,
                ),
            }]

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message(name="assistant"):
            st.toast("Batch response...")
            ai_message: AIMessage = generate_response(messages=st.session_state.messages)
            logger.debug(f"AI message: {ai_message}")
            response = ai_message.content
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

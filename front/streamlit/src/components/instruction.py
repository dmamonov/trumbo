from textwrap import dedent

import streamlit as st


def component() -> None:
    """Main component for the tab."""
    st.header("Using the App")

    st.markdown(dedent(
        """
        ## Knowledge
        Use this to load your script

        ## Chat
        Engage with the chatbot:

        Your conversation (both your input and the assistant's responses) is maintained throughout your session.

        Enjoy exploring the different features of the application!
    """))

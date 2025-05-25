import logging

import streamlit as st


def component() -> None:
    """Main component for the tab."""

    with st.form(key="script") as f_input:

        st.header("Script document")

        text_input = st.text_area(
            label="source",
            placeholder="Paste your script",
            height=400,
            help="Paste your script here. The script will be stored in memory.",
        )

        button = st.form_submit_button("In-memory cache")

        if button:
            try:
                with st.spinner("Processing..."):
                    if not text_input:
                        st.warning("Please provide a script.")
                        return
                    if len(text_input) > 5000:
                        st.warning("Script is too long. Please shorten it.")
                        return
                    if text_input == st.session_state["SCRIPT_TEXT"]:
                        st.warning("Script is already in memory.")
                        return
                    st.toast("Start processing", icon="⏳")
                    st.session_state["SCRIPT_TEXT"] = text_input
                st.toast("Processing done", icon="✅")
                st.success("Processing completed successfully.")
            except Exception as ex:
                st.toast(
                    body="An error occurred while processing the request.",
                    icon="⚠️",
                )
                logging.exception(msg=ex)
                st.exception(ex)

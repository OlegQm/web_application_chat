import pytest
import os
import streamlit as st
from gpt_3.application import Application

@pytest.fixture(scope="module")
def api_key():
    return os.getenv("OPENAI_API_KEY")
    
@pytest.fixture(scope="module")
def application(api_key):
    return Application(api_key)

def test_initial_state(application):
    assert "history" in st.session_state
    assert st.session_state.history == []
    
def test_history_cleaned(application):
    st.session_state.history.append("Test")
    assert len(st.session_state.history) == 1
    application.clear_conversation()
    assert st.session_state.history == []

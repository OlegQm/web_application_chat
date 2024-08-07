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
    assert len(application.bot_instanse.get_formatted_history()) == 0
    
def test_history_cleaned(application):
    application.bot_instanse.ask_bot("Hello!")
    assert len(application.bot_instanse.get_formatted_history()) == 2
    application.clear_conversation()
    assert len(application.bot_instanse.get_formatted_history()) == 0

import pytest
import os
from gpt_3.bot import GPTBot

@pytest.fixture(scope="module")
def api_key() -> str:
    return os.getenv("OPENAI_API_KEY")

@pytest.fixture(scope="module")
def bot(api_key: str) -> GPTBot:
    bot = GPTBot(api_key)
    return bot

def test_bot_answer_length(bot: GPTBot) -> None:
    reply = bot.ask_bot("What is your name?")
    assert len(reply.content) > 0

def test_bot_memory_length(bot: GPTBot) -> None:
    bot.ask_bot("What did I ask you last time?")
    history_messages = bot.get_session_history().messages
    history_messages_length = len(history_messages)
    assert history_messages_length == 4
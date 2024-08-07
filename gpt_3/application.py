import streamlit as st
import os
from gpt_3.bot import GPTBot

@st.cache_resource
def create_bot(api_key: str, model_name: str):
    return GPTBot(api_key, model_name)

class Application():
    def __init__(
            self,
            api_key: str,
            model_name: str = "gpt-3.5-turbo"
    ) -> None:
        self.__bot = create_bot(api_key, model_name)
        if not api_key:
            raise ValueError("API key not found.")
        self.__initialize_interface()
            
    def __initialize_interface(self) -> None:
        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        with col1:
            st.title("**Your personal** AI **assistant**")
        with col2:
            st.button("Clear", on_click=self.clear_conversation)
        st.markdown("---")
            
    def clear_conversation(self) -> None:
        self.__bot.clear_history()
        
    @property
    def bot_instanse(self) -> GPTBot:
        return self.__bot
        
    def initialize_conversation(self) -> None:
        user_message = st.chat_input("Type your message here...")
        if user_message:
            self.__bot.ask_bot(user_message)
            st.markdown("  \n".join(self.__bot.get_formatted_history()))
                   
def main():
    api_key = os.getenv("OPENAI_API_KEY")
    app = Application(api_key)
    app.initialize_conversation()
    
if __name__ == "__main__":
     main()
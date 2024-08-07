import streamlit as st
import os
from gpt_3.bot import GPTBot

@st.cache_resource
def create_bot(api_key: str, model_name: str):
    return GPTBot(api_key, model_name)

class Application():
    def __init__(
            self,
            api_key: str
        ) -> None:
        if not api_key:
            raise ValueError("API key not found.")
        model_name = self.__initialize_interface()
        self.__bot = create_bot(api_key, model_name)
        self.__update_conversation()
            
    def __initialize_interface(self) -> str:
        options = ["gpt-3.5-turbo", "gpt-4o-mini"]
        selected_model = st.selectbox("Choose a model", options)
        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        with col1:
            st.title("**Your personal** AI **assistant**")
        with col2:
            st.button("Clear chat", on_click=self.clear_conversation)
        st.markdown("---")
        return selected_model
            
    def clear_conversation(self) -> None:
        self.__bot.clear_history()
        
    @property
    def bot_instanse(self) -> GPTBot:
        return self.__bot
        
    def __update_conversation(self) -> None:
        user_message = st.chat_input("Type your message here...")
        if user_message:
            self.__bot.ask_bot(user_message)
        st.markdown("  \n".join(self.__bot.get_formatted_history()))
                   
def main():
    api_key = os.getenv("OPENAI_API_KEY")
    app = Application(api_key)
    
if __name__ == "__main__":
     main()
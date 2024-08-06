import streamlit as st
import os
from gpt_3.bot import GPTBot

@st.cache_resource
def create_bot(api_key, model_name):
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
        if "history" not in st.session_state:
            st.session_state.history = []
        self.__initialize_interface()
            
    def __initialize_interface(self) -> None:
        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        with col1:
            st.title("**Your personal** AI **assistant**")
        with col2:
            st.button("Clear", on_click=self.clear_conversation)
        st.markdown("---")
        
    def __get_reply(self, message: str) -> None:  
        response = self.__bot.ask_bot(message)
        return response
            
    def clear_conversation(self) -> None:
        st.cache_resource.clear()
        st.session_state.history = []
        
    def initialize_conversation(self) -> None:
        user_message = st.chat_input("Type your message here...")
        if user_message:
            st.session_state.history.append(f"**You:** {user_message}")
            respose = self.__get_reply(user_message)
            st.session_state.history.append(f"**Bot:** {respose.content}  \n")
            st.markdown("  \n".join(st.session_state.history))
                   
def main():
    api_key = os.getenv("OPENAI_API_KEY")
    app = Application(api_key)
    app.initialize_conversation()
    
if __name__ == "__main__":
     main()
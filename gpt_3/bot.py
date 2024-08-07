from _pytest.mark import deselect_by_keyword
from langchain_openai import ChatOpenAI
from langchain_core.messages.ai import AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
import os

class GPTBot:
    def __init__(
            self,
            api_key: str,
            model_name: str = "gpt-3.5-turbo",
            temperature: float = 0.9
    ) -> None:
        self.__model = model_name
        self.__temperature = temperature
        self.__api_key = api_key
        self.__conversation_history = ChatMessageHistory()
        self.__model_instance = ChatOpenAI(
            model=self.__model,
            temperature=self.__temperature,
            api_key=self.__api_key
        )
        self.__prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You're an assistant."),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ]
        )
        self.__runnable_with_history = RunnableWithMessageHistory(
            runnable=self.__prompt | self.__model_instance,
            get_session_history=self.__get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )

    def __get_session_history(self) -> ChatMessageHistory:
        return self.__conversation_history
    
    def get_formatted_history(self) -> list:
        history = []
        for message in self.__conversation_history.messages:
            if message.type == "human":
                 history.append(f"**You:** {message.content}")
            elif message.type == "ai":
                 history.append(f"**Bot:** {message.content}  \n")
        return history
    
    def clear_history(self) -> None:
        self.__conversation_history = ChatMessageHistory()

    def ask_bot(self, message: str) -> AIMessage:
        response = self.__runnable_with_history.invoke({"input": message})
        return response
    

def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found.")
    bot = GPTBot(api_key)

    messages = [
        "Hello, what is your name?",
        "What did I ask you in previous message?"
    ]
    for message in messages:
        response = bot.ask_bot(message)
        print(response.content, end="\n")

if __name__ == "__main__":
    main()

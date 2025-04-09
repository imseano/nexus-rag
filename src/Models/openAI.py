from Models.model import Model
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()
class openAI(Model):
    def __init__(self):
        self.client = init_chat_model("gpt-3.5-turbo", model_provider="openai")
        super().__init__()

    def constructResponse(self, query: str) -> str:
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=query)
        ]
            
        response = self.client.invoke(messages)

        print(response.content)
        return response.content

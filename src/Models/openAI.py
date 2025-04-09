from Models.model import Model
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
class openAI(Model):
    def __init__(self):
        self.client = init_chat_model("gpt-3.5-turbo", model_provider="openai")
        super().__init__()

    def constructResponse(self, query: list[str]) -> str:
        #if (len(query) == 1):
           # messages = [
           #     SystemMessage(content="You are a helpful assistant."),
          #      HumanMessage(content=query)
         #   ]
       # elif (len(query) <= 0):
        #    raise ValueError("Query cannot be empty.")
         
        response = self.client.invoke(query)

        print(response.content)
        return response.content

class openAIEmbed():

    def __init__(self):
         self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
   
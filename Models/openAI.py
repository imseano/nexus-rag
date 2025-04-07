from model import Model
from openai import OpenAI

class openAI(Model):
    def __init__(self):
        self.client = OpenAI()
        super().__init__()

    def constructResponse(self, query: str) -> str:
            
        response = self.client.responses.create(
            model="gpt-4o",
            input=query
        )

        print(response.output_text)
        return response.output_text

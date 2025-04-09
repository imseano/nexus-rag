from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def constructResponse(self, query: str) -> str:
        pass

    def acceptquery(self, query: str):
        if (len(query) <= 0):
            print("no query")
            return 0
        response = self.constructResponse(query)

        return response



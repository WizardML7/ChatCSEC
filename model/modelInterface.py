from abc import ABC, abstractmethod

class iModel(ABC):
    @abstractmethod
    def prompt(self, context:str, prompt:str):
        pass
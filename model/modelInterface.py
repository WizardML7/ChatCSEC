from abc import ABC, abstractmethod

class iModel(ABC):
    @abstractmethod
    def prompt(self, system:str, context:str, prompt:str):
        pass
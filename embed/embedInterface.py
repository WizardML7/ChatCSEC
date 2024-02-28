from abc import ABC, abstractmethod

class iEmbed(ABC):
    @staticmethod
    @abstractmethod
    def createEmbedding(content) -> list:
        pass

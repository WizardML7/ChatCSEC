from abc import ABC, abstractmethod

class iEmbed(ABC):
    @abstractmethod
    def createEmbedding(self, content):
        pass

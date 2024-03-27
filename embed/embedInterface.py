from abc import ABC, abstractmethod

class iEmbed(ABC):
    @staticmethod
    @abstractmethod
    def createEmbedding(content: str, maxChunkSize: int, chunkOverlap: int, delimiter: str) -> dict:
        pass

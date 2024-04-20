from abc import ABC, abstractmethod

class iEmbed(ABC):
    """
    An interface used for all embedding models to support dependency injection, inversion and
    polymorphism throughout the application.
    """
    @abstractmethod
    def createEmbedding(content: str, maxChunkSize: int, chunkOverlap: int, delimiter: list) -> dict[str, list[float]]:
        """
        Takes in a string, chunks the string and embeds the chunks.
        Args:
            content (str): The string to be embedded.
            maxChunkSize (int): The max size chunks should be.
            chunkOverlap (int): The overlap between chunks.
            delimiter (list): A list of delimiters that the splitter should chunk on.

        Returns:
            dict: a dictionary of all split chunks as keys and corresponding embeddings as values.
        """
        pass

from abc import ABC, abstractmethod

class iVectorDB(ABC):
    """
    An interface for databases to support dependency injection, inversion and polymorphism throughout the project.
    All databases defined for use with this application should confirm to this interface"
    """
    @abstractmethod
    def createCollection(self, collectionName: str, size: int):
        """
        Create a new collection to store objects in a database
        Args:
            collectionName (str): The identifier for the collection to create.
            size (int): The size of the vectors to be stored in the collection.

        Returns:
            None
        """
        pass

    @abstractmethod
    def saveToDB(self, texts: dict, collectionName: str):
        """
        Saves a collection of text-embedding combinations to the database under a specified collection
        Args:
            texts (dict): A dictionary with the keys being a text and the value being the embedding vector representing
            the key.
            collectionName (str): The collection identifier to store the strings under.

        Returns:
            None
        """
        pass

    @abstractmethod
    def queryDB(self, embedding: list[float],
                collectionNames: list[str]=None, maxHits: int=100, minSimilarity: float=0) -> list:
        """
        Queries the database for similar vectors to the provided embedding vector.

        Args:
            embedding (list): A list of embeddings to use for semantic searching in the vector database.
            collectionNames (list): A list of collection identifiers to search with the provided embedding.
            maxHits (list): The max amount of results to be returned yb the query.
            minSimilarity (float): The required minimum similarity to be returned by the query.

        Returns:
            list: A list of results from the query
        """
        pass

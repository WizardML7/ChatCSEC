from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from .DBInterface import iVectorDB
class QDrantVectorDB(iVectorDB):
    """
    Class representing a connection to an instance of a QDrant Vector Database
    """
    def __init__(self, host: str):
        """
        Constructor for database
        Args:
            host (str): The ip address of the qdrant instance. Can also specify ":memory:" to create an instance in
            RAM. Due to the nature of databases, this is not recommended outside of testing.
        """
        self.client = QdrantClient(host=host, prefer_grpc=True, timeout=None)

    def createCollection(self, collectionName: str, size: int):
        """
        Create a collection in the vector database.

        Args:
            collectionName (str): The identifier for the new collection.
            size (int): The size of the embedding vectors that will be stored in the database.

        Returns:
            None
        """
        self.client.recreate_collection(
            collection_name=collectionName,
            vectors_config={"text embedding" : models.VectorParams(
                size=size,
                distance=models.Distance.COSINE
            )}
        )


    def convertToPoints(self, texts: dict) -> list[PointStruct]:
        """
        Converts a dictionary of text-embedding key-value pairs to a list of PointStructs to store in the DB.

        Args:
            texts (dict): A text-embedding key-value dictionary to convert into PointStructs .

        Returns:
            list: A list of PointStructs.

        """
        return [
            PointStruct(id=idx,
                        vector={"text embedding": embedding.result()},
                        payload={"text": text},
                        )
            for idx, (embedding, text) in enumerate(zip(texts.values(), texts.keys()))
        ]


    def saveToCollection(self, collectionName: str, points: list[PointStruct]):
        """
        Save a list of points to the database under a specific collection.

        Args:
            collectionName (str): The identifier of the collection to save the points to.
            points (list): A list of PointStructs to save to the database

        Returns:
            None
        """
        self.client.upsert(collectionName, points)

    #Texts is a dict combo of text and embeddings output from an embedding model
    def saveToDB(self, texts: dict, collectionName: str):
        """
        Save a collection of text-embedding combinations to a collection in the database.

        Args:
            texts (dict):  A text-embedding key-value dictionary to convert into PointStructs.
            collectionName (str): The identifier of the collection to save the points to.

        Returns:

        """
        points = self.convertToPoints(texts)
        self.saveToCollection(collectionName, points)

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

        TODO:
            Change to return normalized data instead of ScoredPoints

        """
        results = []
        if not collectionNames:
            collectionNames = [collection['name'] for collection in self.client.get_collections().dict()['collections']]

        # TODO: make sure to only search collections of the proper size
        for collection in collectionNames:
            results.append(self.client.search(collection_name=collection,
                                              query_vector=("text embedding", embedding.result()),
                                              limit=maxHits,
                                              score_threshold=minSimilarity
                                              ))

        return results

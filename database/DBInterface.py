from abc import ABC, abstractmethod

class iDB(ABC):

    @abstractmethod
    def createCollection(self, collectionName: str, size: int):
        pass

    @abstractmethod
    def saveToDB(self, texts: dict, collectionName: str):
        pass

    @abstractmethod
    def queryDB(self, query):
        pass

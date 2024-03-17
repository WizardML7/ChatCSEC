from abc import ABC, abstractmethod

class iDB(ABC):
    @abstractmethod
    def saveToDB(self, texts: dict, collectionName: str):
        pass

    @abstractmethod
    def queryDB(self, query):
        pass

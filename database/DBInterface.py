from abc import ABC, abstractmethod

class iDB(ABC):
    @abstractmethod
    def saveToDB(self, data):
        pass

    @abstractmethod
    def queryDB(self, query):
        pass

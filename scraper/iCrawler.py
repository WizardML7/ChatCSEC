from abc import ABC, abstractmethod

class ICrawler(ABC):
    @abstractmethod
    def crawl(url: str, maxDepth: int, baseDirectory: str, cores: int, outputDirectory: str) -> set:
        pass
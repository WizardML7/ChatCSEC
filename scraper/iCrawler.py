from abc import ABC, abstractmethod

class iCrawler(ABC):
    '''
    Interface created for crawlers to inherit to support dependency inversion and injection into the main class.  This
    was used to give easy flexibility of mixing and matching components for ease of performance testing. All crawlers
    should be written to conform to this interface in order to function properly with the rest of the application."
    '''
    @abstractmethod
    def crawl(url: str, maxDepth: int, baseDirectory: str, cores: int, outputDirectory: str, urlRegexString: str,
              contentRegexString: str, matchSkip: bool) -> set:
        pass
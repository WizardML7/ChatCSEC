from abc import ABC, abstractmethod

class iCrawler(ABC):
    """
    Interface created for crawlers to inherit to support dependency inversion and injection into the main class.  This
    was used to give easy flexibility of mixing and matching components for ease of performance testing. All crawlers
    should be written to conform to this interface in order to function properly with the rest of the application."
    """
    @abstractmethod
    def crawl(url: str, maxDepth: int, baseDirectories: list[str], cores: int, outputDirectory: str, urlRegexString: str,
              contentRegexString: str, matchSkip: bool) -> set:
        """Method to start crawling webpoages and downloading related content.

        Notes:
            It is important to use theContentRegexString argument in order to properly sanitize irrelevant information
            such as website navbars, headers and footers.  This content can be detrimental to the results of the
            embedding and retrieval in the RAG prompts, as well as increasing the token burden on API calls.

        Args:
            maxDepth (int): The max depth that the crawler should follow links to
            baseDirectories (list): A list of URLs that specify the allowed url directories that the crawler will pull
                webpages from.  If this is set to None, all URLs will be accepted.
            cores (int): The amount of CPU cores for the crawler to use
            outputDirectory (str): A path pointing to the output directory for the files downloaded and processed
            urlRegexString (str): A string representing a regex to match URLs with.  If set to None, all URLs will be
                accepted for download
            contentRegexString (str): A regex used to extract content out of webpages.  It must follow the syntax of
                (?:.LOOKABEHIND)(?P<content>.*)(?:LOOKBEHIND). If set to None, all content will be ingested
            matchSkip (bool): If set to True, any content that does not match the contentRegexString will not be
                downloaded. If contentRegexString is set to None, this variable is not used.

        Returns:
            Set: A set of links found by the crawler.

        Examples:
            >>> Crawler.crawl("https://openai.com/customer-stories", 1,
            >>>     cores=4, baseDirectory=["https://openai.com/customer-stories"],
            >>>     outputDirectory=os.path.dirname(os.path.realpath(__file__)) + "/test/",
            >>>     urlRegexString=r'.*customer-stories.*a.*',
            >>>     contentRegexString=r'(?:.*Customer stories)(?P<content>.*)(?:ResearchOverviewIndexGP.*)',
            >>>     matchSkip=True)
        """
        pass
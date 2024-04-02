import requests
from pathvalidate import sanitize_filepath
from urllib.parse import urlparse
import os
from .iCrawler import iCrawler
from multiprocessing import Pool, Manager
from .handlers import PDFHandler, HTMLHandler
import traceback
import re
from queue import Empty

class Crawler(iCrawler):
    @staticmethod
    def crawlPage(local_domain: str, url: str, depth: int,maxDepth: int, baseDirectory: str, queue, seen,
                  outputDirectory: str, recordUrl: bool, contentRegex: re.Pattern, matchSkip: bool=False):
        print(url, depth)  # for debugging and to see the progress
        # Try extracting the text from the link, if failed proceed with the next item in the queue

        # Handler Mappings
        handlers = {
            "application/pdf": PDFHandler,
            "text/html": HTMLHandler
        }

        content = requests.get(url)
        contentType = content.headers["content-type"].split(";")[0]

        if recordUrl:
            try:
                # Save text from the url to a <url>.txt file
                # TODO: Fix bug with bad filenames, try first openai test for example
                filename = sanitize_filepath(outputDirectory + '/text/' + local_domain + '/' + url[8:].replace("/", "_") + ".txt")
                with open(filename, "w", encoding="UTF-8") as f:
                    # use the appropriate handler for the MIME type
                    try:
                        text = handlers[contentType].parseText(content)
                    except KeyError:
                        print(f'{url} requires {contentType} handler, not implemented')
                        return

                    # If the crawler gets to a page that requires JavaScript, it will stop the crawl
                    if ("You need to enable JavaScript to run this app." in text):
                        print("Unable to parse page " + url + " due to JavaScript being required")
                        return

                    if contentRegex:
                        group = contentRegex.search(text)
                        if not matchSkip and not group:
                            Exception(f"{url} doe snot match regex, skipping write")
                        elif group:
                            f.write(group['content'])
                    else:
                        f.write(text)

            except Exception as e:
                traceback.print_exc()
                print("Unable to parse page " + url)

        # Get the hyperlinks from the URL and add them to the queue
        if depth < maxDepth:
            handlers[contentType].findLinks(content, local_domain, seen, queue, depth, baseDirectory)

    @staticmethod
    def crawl(url: str, maxDepth: int,baseDirectories: list[str] = None, cores: int = 2,
              outputDirectory: str = os.path.dirname(os.path.realpath(__file__)),
              urlRegexString: str=None, contentRegexString: str=None, matchSkip: bool=False) -> set:
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

        if urlRegexString:
            urlRegex = re.compile(urlRegexString)

        contentRegex = None
        if contentRegexString:
            contentRegex = re.compile(contentRegexString)

        # Create a directory to store the text files
        if not os.path.exists(outputDirectory + "/text/"):
            os.makedirs(outputDirectory + "/text/")

        # Create a directory to store the csv files
        if not os.path.exists(outputDirectory + "/processed/"):
            os.makedirs(outputDirectory + "/processed/")

        # While the queue is not empty, continue crawling
        with Manager() as manager, Pool(processes=cores) as pool:
            # Create a queue to store the URLs to crawl
            queue = manager.Queue()
            # Create a set to store the URLs that have already been seen (no duplicates)
            # Using a dict as a set, since there is no manager.set()
            seen = manager.dict()
            queue.put((url, 0))
            seen[url] = 1
            results = []

            while True:
                # Get the next URL from the queue
                try:
                    next = queue.get_nowait()
                    url = next[0]
                    depth = next[1]
                    recordURL = True
                    # Parse the URL and get the domain
                    local_domain = urlparse(url).netloc

                    if urlRegexString and not urlRegex.match(url):
                        recordURL = False

                    if not os.path.exists(outputDirectory + "/text/" + local_domain + "/") and recordURL:
                        os.mkdir(outputDirectory + "/text/" + local_domain + "/")

                    results.append(pool.apply_async(Crawler.crawlPage,
                                                    (local_domain, url, depth, maxDepth, baseDirectory, queue, seen,
                                                     outputDirectory, recordURL, contentRegex, matchSkip)))
                except Empty:
                    results = [res for res in results if not res.ready()]
                    if len(results) == 0 and queue.empty():
                        break
            foundLinks = set(seen.keys())
        return foundLinks


def testInterface(crawler: iCrawler):
    # OpenAI Test
    Crawler.crawl("https://openai.com/", 1, cores=4)
    # OpenAI Customer Stories test
    # Crawler.crawl("https://openai.com/customer-stories", 1, cores=4, baseDirectory=["https://openai.com/customer-stories"], outputDirectory=os.path.dirname(os.path.realpath(__file__)) + "/test/", urlRegexString=r'.*customer-stories.*a.*', contentRegexString=r'(?:.*Customer stories)(?P<content>.*)(?:ResearchOverviewIndexGP*)')
    # PDF Test
    # Crawler.crawl("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-28.pdf", 1, baseDirectory=["https://doi.org", "https://nvlpubs.nist.gov"], cores=4)


# Test function
if __name__ == "__main__":
    testInterface(Crawler)


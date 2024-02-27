import requests

from urllib.parse import urlparse
import os
from iCrawler import ICrawler
from multiprocessing import Pool, cpu_count, Manager
from handlers import PDFHandler, HTMLHandler
import traceback



class Crawler(ICrawler):
    @staticmethod
    def crawlPage(local_domain: str, url: str, depth: int, maxDepth: int, baseDirectory: str, queue, seen):
        print(url, depth)  # for debugging and to see the progress
        # Try extracting the text from the link, if failed proceed with the next item in the queue

        # Handler Mappings
        handlers = {
            "application/pdf": PDFHandler,
            "text/html": HTMLHandler
        }

        try:
            # Save text from the url to a <url>.txt file
            # TODO: Fix bug with bad filenames, try first openai test for example
            with open('text/' + local_domain + '/' + url[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:
                content = requests.get(url)
                contentType = content.headers["content-type"].split(";")[0]
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

                # Otherwise, write the text to the file in the text directory
                f.write(text)

        except Exception as e:
            traceback.print_exc()
            print("Unable to parse page " + url)

        # Get the hyperlinks from the URL and add them to the queue
        if depth < maxDepth:
            handlers[contentType].findLinks(content, local_domain, seen, queue, depth, baseDirectory)

    @staticmethod
    def crawl(url: str, maxDepth: int, baseDirectory: list[str]=None, cores: int=2) -> set:

        # Create a directory to store the text files
        if not os.path.exists("text/"):
            os.mkdir("text/")

        # Create a directory to store the csv files
        if not os.path.exists("processed"):
            os.mkdir("processed")

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

                    # Parse the URL and get the domain
                    local_domain = urlparse(url).netloc

                    if not os.path.exists("text/" + local_domain + "/"):
                        os.mkdir("text/" + local_domain + "/")

                    results.append(pool.apply_async(Crawler.crawlPage,
                                                    (local_domain, url, depth, maxDepth, baseDirectory, queue, seen)))
                except:
                    results = [res for res in results if not res.ready()]
                    if len(results) == 0 and queue.empty():
                        break
            foundLinks = set(seen.keys())
        return foundLinks

def testInterface(crawler: ICrawler):
    # OpenAI Test
    Crawler.crawl("https://openai.com/customer-stories", 1, cores=4)
    # OpenAI Customer Stories test
    # Crawler.crawl("https://openai.com/customer-stories", 1, cores=4, baseDirectory=["https://openai.com/customer-stories"])
    # PDF Test
    # Crawler.crawl("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-28.pdf", 1, baseDirectory=["https://doi.org", "https://nvlpubs.nist.gov"], cores=4)

# Test function
if __name__ == "__main__":
    testInterface(Crawler)


from abc import ABC, abstractmethod
from requests.models import Response
from pypdf import PdfReader
from io import BytesIO
import re
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from html.parser import HTMLParser
from queue import Queue
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.opc.constants import RELATIONSHIP_TYPE as RELTYPES

HTTP_URL_PATTERN = r'^http[s]{0,1}://.+$'
PROTOCOL_BLACKLIST = ["#", "mailto:", "tel:"]


class IHandler(ABC):
    """
    Interface created for different handlers to be used by the crawler, used to support polymorphism and handle
    multiple filetypes.
    """
    @staticmethod
    @abstractmethod
    def parseText(content: Response) -> str:
        """
        Parse the content retrieved from a webpage.

        Args:
            content (Response): A response object returned from the requests library.
        Returns:
            str: The content represented in a textual format.
        """
        pass

    @staticmethod
    @abstractmethod
    def findLinks(content: Response, local_domain: str, seen: dict,
                  queue: Queue, depth: int, baseDirectories: list[str]):
        """
        Method to find all non-blacklisted links from documents

        Args:
            content (Response): A response object returned from the requests library.
            local_domain (str): The net location of the URL.
            seen (dict): A dictionary containing the currently viewed links as keys.  This is a dictionary instead of a
                set as the manager for multiprocessing does not support the Set type.
            queue (Queue): The queue for the crawler to search new links.
            depth (int): The current depth of the crawl operation.
            baseDirectories (list): A list of accepted URLs for the crawler to search and save.
        """
        pass

    @staticmethod
    @abstractmethod
    def addLinks(links: list[str], seen: dict, queue: Queue, depth: int, baseDirectories: list[str]):
        """
        Generic method for classes to add found links to the queue for workers to process later. The method will first
        check to see if any of the links have already been seen before adding to the queue.

        Args:
            links (list): list of URLs to attempt to add to the worker queue.
            seen (dict): A dictionary containing the currently viewed links as keys.  This is a dictionary instead of a
                set as the manager for multiprocessing does not support the Set type.
            queue (Queue): The queue for the crawler to search new links.
            depth (int): The current depth of the crawl operation.
            baseDirectories (list): A list of accepted URL directories for the crawler to search and save.
        """
        if not baseDirectories:
            baseDirectories = ["http"]
        for link in links:
            if link not in seen.keys() and link.startswith(tuple(baseDirectories)):
                queue.put((link, depth + 1))
                seen[link] = 1



class HTMLHandler(IHandler):
    """
    HTML handler for the crawler to use for processing documents.
    """
    class HyperlinkParser(HTMLParser):
        """
        Subclass used to handle hyperlink parsing for HTML documents.
        """
        def __init__(self):
            super().__init__()
            # Create a list to store the hyperlinks
            self.hyperlinks = []

        # Override the HTMLParser's handle_starttag method to get the hyperlinks
        def handle_starttag(self, tag: str, attrs: dict):
            """
            Method used to account for HTML tags, attempts to find hrefs.

            Args:
                tag (str): The tag of the HTML element.
                attrs (dict): The attributes of the HTML element.
            """
            attrs = dict(attrs)

            # If the tag is an anchor tag and it has an href attribute, add the href attribute to the list of hyperlinks
            if tag == "a" and "href" in attrs:
                self.hyperlinks.append(attrs["href"])

    @staticmethod
    def parseText(content: Response) -> str:
        """
        Extracts text from the response passed to the method.

        Args:
            content (Response): A response received from the requests library with HTML content type.

        Returns:
            str: The textual representation of the HTML page.
        """
        return BeautifulSoup(content.text, "html.parser").get_text()

    @staticmethod
    def get_hyperlinks(content: Response):
        """
        Retrieves the hyperlinks found in the HTML document.

        Args:
            content (Response): A response received from the request library with the html content type.
        """
        # Try to open the URL and read the HTML
        try:
            html = content.content.decode('utf-8')
        except Exception as e:
            print(e)
            return []

        # Create the HTML Parser and then Parse the HTML to get hyperlinks
        parser = HTMLHandler.HyperlinkParser()
        parser.feed(html)

        return parser.hyperlinks

    # Function to get the hyperlinks from a URL that are within the same domain
    @staticmethod
    def get_clean_hyperlinks(local_domain: str, content: Response) -> list[str]:
        """
        Method used to get allowed hyperlinks.

        Args:
            local_domain (str): The domain of the current URL.
            content (Response): A response received from the request library with the html content type.

        Returns:
            list: A list of allowed hyperlinks found on the provided page.
        """
        clean_links = []
        for link in set(HTMLHandler.get_hyperlinks(content)):
            # If the link is a URL, check if it is within the same domain
            if re.search(HTTP_URL_PATTERN, link):
                clean_link = link
            # If the link is not a URL, check if it is a relative link
            else:
                if link.startswith("/"):
                    link = link[1:]
                elif link.startswith(tuple(PROTOCOL_BLACKLIST)):
                    continue
                clean_link = "https://" + local_domain + "/" + link

            if clean_link is not None:
                if clean_link.endswith("/"):
                    clean_link = clean_link[:-1]
                clean_links.append(clean_link)

        # Return the list of hyperlinks that are within the same domain
        return list(set(clean_links))

    @staticmethod
    def findLinks(content: Response, local_domain: str, seen, queue, depth, baseDirectories: list[str]):
        """
        Finds all allowed links on a given page and adds them to the Queue for workers to continue processing

        Args:
            content (Response):  A response received from the request library with the html content type.
            local_domain (str): The domain of the current URL.
            seen (dict): A dictionary containing the currently viewed links as keys.  This is a dictionary instead of a
                set as the manager for multiprocessing does not support the Set type.
            queue (Queue): The queue for the crawler to search new links.
            depth (int): The current depth of the crawl operation.
            baseDirectories (list): A list of accepted URL directories for the crawler to search and save.
        """
        links = HTMLHandler.get_clean_hyperlinks(local_domain, content)
        HTMLHandler.addLinks(links, seen, queue, depth, baseDirectories)


class PDFHandler(IHandler):
    """
    Handler for the crawler to use for PDF documents.
    """
    @staticmethod
    def parseText(content: Response) -> str:
        """
        Extracts text from provided PDF files returned from the request library.

        Args:
            content (Response):  A response received from the request library with the PDF content type.

        Returns:
            str: The extracted textual representation of the PDF file.
        """
        text = ""
        reader = PdfReader(BytesIO(content.content))
        for page in reader.pages:
            text += page.extract_text()
        return text

    @staticmethod
    def findLinks(content: Response, local_domain: str, seen: dict,
                  queue: Queue, depth: int, baseDirectories: list[str]):
        """
        Finds all links within a PDF file and adds them to a queue for the workers to continue searching through.

        Args:
            content (Response): A response received from the request library with the PDF content type.
            local_domain (str): The domain of the current URL being analyzed.
            seen (dict):  A dictionary containing the currently viewed links as keys.  This is a dictionary instead of a
                set as the manager for multiprocessing does not support the Set type.
            queue (Queue): The queue for the crawler to search new links.
            depth (int): The current depth of the crawl operation.
            baseDirectories (list): A list of accepted URL directories for the crawler to search and save.
        """

        links = []
        reader = PdfReader(BytesIO(content.content))
        pages = len(reader.pages)
        key = '/Annots'
        uri = '/URI'
        ank = '/A'

        for page in range(pages):
            pageSliced = reader.pages[page]
            pageObject = pageSliced.get_object()
            if key in pageObject.keys():
                ann = pageObject[key]
                for a in ann:
                    u = a.get_object()
                    if uri in u[ank].keys() and not uri.startswith(tuple(PROTOCOL_BLACKLIST)):
                        links.append(u[ank][uri])

        PDFHandler.addLinks(links, seen, queue, depth, baseDirectories)


class WordHandler(IHandler):
    """
    Handler for the crawler to use to parse docx files
    """
    @staticmethod
    def parseText(content) -> str:
        """
        Extract the text from the docx document

        Args:
            content: A response received from the request library with the docx content type.

        Returns:
            str: The text and tables in the docx file
        """
        document = Document(BytesIO(content.content))
        text = ''
        for obj in document.iter_inner_content():
            if type(obj) == Table:
                widths = dict()
                #Get max width of each column
                for index in range(len(obj.columns)):
                    for cell in obj.column_cells(index):
                        if cell.width not in widths.keys():
                            widths[cell.width] = len(cell.text.replace("\n", " "))
                        elif len(cell.text) > widths[cell.width]:
                            widths[cell.width] = len(cell.text.replace("\n", " "))
                #Add each cell and format
                for index in range(len(obj.rows)):
                    text += "|"
                    for cell in obj.row_cells(index):
                        stripped = cell.text.replace("\n", " ")
                        text += f'{stripped:<{widths[cell.width]}}' + "|"
                    text += "\n"
            elif type(obj) == Paragraph:
                text += obj.text + "\n\n"

        return text

    @staticmethod
    def findLinks(content: Response, local_domain: str, seen: dict,
                  queue: Queue, depth: int, baseDirectories: list[str]):
        """
        Finds all links within a docx file and adds them to a queue for the workers to continue searching through.

        Args:
            content (Response): A response received from the request library with the PDF content type.
            local_domain (str): The domain of the current URL being analyzed.
            seen (dict):  A dictionary containing the currently viewed links as keys.  This is a dictionary instead of a
            set as the manager for multiprocessing does not support the Set type.
            queue (Queue): The queue for the crawler to search new links.
            depth (int): The current depth of the crawl operation.
            baseDirectories (list): A list of accepted URL directories for the crawler to search and save.

        Returns:
            None
        """
        document = Document(BytesIO(content.content))
        links = []
        # undocumented in api reference, black magic in the docx library
        # rels comes from
        for relation in document.part.rels:
            if relation.reltype == RELTYPES.HYPERLINK:
                links.append(relation.target_part())

        WordHandler.addLinks(links, seen, queue, depth, baseDirectories)

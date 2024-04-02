from openai import OpenAI
from .embedInterface import iEmbed
from .embedPrepper import EmbedPrepper
import requests
from bs4 import BeautifulSoup

class OpenAIEmbed(iEmbed):
    """
    Impelementation of OpenAI's embedding model
    """

    @staticmethod
    def embedChunk(content: str, client: OpenAI) -> list:
        """
        Creates an embedding vector of a chunk of data.

        Args:
            content (str): A chunk of text to embed
            client (OpenAI): An OpenAI client object used to make the embedding call

        Returns:
            list: An embedding vector representing the content

        TODO:
            Make client calls async to speed up the applications embedding process
        """
        response = client.embeddings.create(
            input=content,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    @staticmethod
    def createEmbedding(content: str, maxChunkSize: int=800, chunkOverlap: int=100, delimiter: str="\n") -> dict:
        """
        Creates a collection of embeddings by chunking the provided content and embedding each of those chunks

        Args:
            content (str): The string to be embedded.
            maxChunkSize (int): The max size chunks should be.
            chunkOverlap (int): The overlap between chunks.
            delimiter (list): A list of delimiters that the splitter should chunk on.

        Returns:
            dict: a dictionary of all split chunks as keys and corresponding embeddings as values.

        TODO:
            Investigate the whitespace for chunking.
            Improve the method by which text is chunked.  I believe this will be the biggest impact on results of the
            application.
        """
        client = OpenAI()
        chunks = EmbedPrepper.chunkTextBySize(content, maxChunkSize, chunkOverlap, delimiter)
        embeddingMap = dict()

        for chunk in chunks:
            # print(chunk)
            embeddingMap[chunk] = OpenAIEmbed.embedChunk(chunk, client)

        return embeddingMap




if __name__ == "__main__":
    # embedding test
    # print(OpenAIEmbed.createEmbedding("asdf"))
    # chunk test
    # print(EmbedPrepper.chunkTextBySize(BeautifulSoup(requests.get("https://www.nist.gov/publications/non-fungible-token-security").text, "html.parser").get_text()))
    # Whitespace text
    # print(EmbedPrepper.removeExtraWhitespace("Hello     \n\n this     is a test   for extra whitespace."))
    # int test
    # for i,v in OpenAIEmbed.createEmbedding(BeautifulSoup(requests.get("https://www.nist.gov/publications/non-fungible-token-security").text, "html.parser").get_text()).items():
    #     print(f"key:{i}")
    #     print(f"value: {v}")
    pass

import os

from openai import AsyncOpenAI
from .embedInterface import iEmbed
from .embedPrepper import EmbedPrepper
import asyncio
import sys

class OpenAIEmbed(iEmbed):
    """
    Implementation of OpenAI's embedding model
    """
    def __init__(self, model: str):
        """
        Constructor for openAIEmbed
        Args:
            model (str): The identifier for the model to be used. Model identifiers can be found
            at https://platform.openai.com/docs/models/embeddings
        """
        self.client = AsyncOpenAI()
        self.model = model

    async def embedChunk(self, content: str) -> list:
        """
        Creates an embedding vector of a chunk of data.

        Args:
            content (str): A chunk of text to embed

        Returns:
            list: An embedding vector representing the content
        """
        response = await self.client.embeddings.create(
            input=content,
            model=self.model
        )
        return response.data[0].embedding

    async def createEmbedding(self, content: str, maxChunkSize: int=800, chunkOverlap: int=100, delimiter: str=["\n\n", "\n", " ", ""]) -> dict:
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
        content = EmbedPrepper.removeExtraWhitespace(content)
        chunks = EmbedPrepper.chunkTextBySize(content, maxChunkSize, chunkOverlap, delimiter)
        embeddingMap = dict()

        for chunk in chunks:
            # print(chunk)
            embeddingMap[chunk] = asyncio.ensure_future(self.embedChunk(chunk))

        await asyncio.gather(*list(embeddingMap.values()))
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

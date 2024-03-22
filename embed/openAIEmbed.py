from openai import OpenAI
from .embedInterface import iEmbed
from .embedPrepper import EmbedPrepper
import requests
from bs4 import BeautifulSoup

class OpenAIEmbed(iEmbed):
    @staticmethod
    def embedChunk(content: str, client: OpenAI) -> list:
        # TODO: make async, is very slow :(
        response = client.embeddings.create(
            input=content,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    @staticmethod
    def createEmbedding(content: str, maxChunkSize: int=800, chunkOverlap: int=100, delimiter: str="\n") -> dict:
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

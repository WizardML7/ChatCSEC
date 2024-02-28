from openai import OpenAI
from embedInterface import iEmbed
from embedPrepper import EmbedPrepper
import os
class OpenAIEmbed(iEmbed):
    @staticmethod
    def embedChunk(content: str, client: OpenAI) -> list:
        response = client.embeddings.create(
            input=content,
            model="text-embedding-3-small"
        )
        print(type(response.data[0].embedding))
        return response.data[0].embedding

    @staticmethod
    def createEmbedding(content: str) -> list:
        client = OpenAI()



if __name__ == "__main__":
    # embedding test
    # print(OpenAIEmbed.createEmbedding("asdf"))
    # chunk test
    # print(EmbedPrepper.chunkText("Be not afraid of greatness. Some are born great, some achieve greatness, and others have greatness thrust upon them." * 4, 5, "."))
    # Whitespace text
    # print(EmbedPrepper.removeExtraWhitespace("Hello     \n\n this     is a test   for extra whitespace."))
    pass
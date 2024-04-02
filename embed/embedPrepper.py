from typing import Callable
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

class EmbedPrepper:
    """
    A collection of methods used to prepare text to be embedded by embedding models

    TODO:
        Find better methods of chunking.  Ideally finding a way to chunk by semantic relevance would produce the best
        effects.  Mi
    """
    @staticmethod
    def chunkTextBySize(content: str, maxChunkSize: int=800,
                        chunkOverlap: int=100, delimiter: list=["\n\n", "\n", " ", ""]) -> list:
        """
        Chunks text by the given delimiters aiming for a maximum size per chunk.

        Args:
            content (str): The string to turn into chunks
            maxChunkSize (int): The maximum size for chunks to be
            chunkOverlap (int): The amount of text for the chunks to overlap with
            delimiter (list): A list of delimiters for the splitter to split on

        Returns:
            list: List of chunks from the text
        """
        text_splitter = RecursiveCharacterTextSplitter(
            separators=delimiter,
            chunk_size=maxChunkSize,
            chunk_overlap=chunkOverlap,
            length_function=len,
        )
        # print(content)
        chunks = text_splitter.split_text(content)
        return chunks

    @staticmethod
    def removeExtraWhitespace(content: str) -> str:
        """
        A method to remove the extra whitespace from a string
        Args:
            content (str): a string to rmeove whitespace from

        Returns:
            str: The content string stripped of newlines
        """
        content = content.replace("\n", " ")\
                    .replace("\r", " ")\
                    .replace("\xa0", " ")

        while content.find("  ") != -1:
            content = content.replace("  ", " ")
        return content

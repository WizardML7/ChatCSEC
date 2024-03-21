from typing import Callable
import tiktoken
from langchain.text_splitter import CharacterTextSplitter

class EmbedPrepper:
    @staticmethod
    def chunkTextBySize(content: str, maxChunkSize: int=800, chunkOverlap: int=100, delimiter: str="\n") -> list:
        text_splitter = CharacterTextSplitter(
            separator=delimiter,
            chunk_size=maxChunkSize,
            chunk_overlap=chunkOverlap,
            length_function=len,
        )
        chunks = text_splitter.split_text(content)
        return chunks
    @staticmethod
    def removeExtraWhitespace(content: str) -> str:
        content = content.replace("\n", " ")\
                    .replace("\r", " ")\
                    .replace("\xa0", " ")

        while content.find("  ") != -1:
            content = content.replace("  ", " ")
        return content

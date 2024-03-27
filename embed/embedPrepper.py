from typing import Callable
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

class EmbedPrepper:
    @staticmethod
    def chunkTextBySize(content: str, maxChunkSize: int=800, chunkOverlap: int=100, delimiter: list=["\n\n", "\n", " ", ""]) -> list:
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
        content = content.replace("\n", " ")\
                    .replace("\r", " ")\
                    .replace("\xa0", " ")

        while content.find("  ") != -1:
            content = content.replace("  ", " ")
        return content

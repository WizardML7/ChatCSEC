class EmbedPrepper:
    @staticmethod
    def chunkText(content: str, maxChunkSize: int, delimiter: str) -> list:
        chunks = content.split(delimiter)
        for chunkIndex, chunk in enumerate(chunks):
            if len(chunk) > maxChunkSize:
                newChunks = [chunk[index: index + maxChunkSize] for index in range(0, len(chunk), maxChunkSize)]
                chunks.remove(chunk)
                for index in range(len(newChunks)):
                    chunks.insert(chunkIndex + index, newChunks[index])
        return chunks
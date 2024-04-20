from database.DBInterface import iVectorDB
from database.QDrantDB import QDrantVectorDB
from embed.embedInterface import iEmbed
from embed.openAIEmbed import OpenAIEmbed
from model.modelInterface import iModel
from model.GPT import GPT
from scraper.iCrawler import iCrawler
from scraper.crawler import Crawler
from multiprocessing import cpu_count

import asyncio
import os
import sys
from time import perf_counter


async def run(db: iVectorDB, embed: iEmbed, model: iModel, crawler: iCrawler):
    """
    Test function to show a static run through of the workflow of the application.  This function will create a new
    database collection crawl a webpage, create embeddings, save the embedding vectors and content, and perform a RAG
    prompt. To support modularity, the application ahs been designed with dependency injection in mind.

    Args:
        db (iVectorDB): A database object that conforms to the iDB interface
        embed (iEmbed): An embed object that conforms to the iEmbed interface
        model (iModel): A model object that conforms to the ICrawler interface
    """
    prompt = "What is CVE-2024-29943?"

    start = perf_counter()
    collectionName = "asd"
    db.createCollection(collectionName, 1536)

    outputDir = "./data/"
    '''
    crawler.crawl("https://www.mozilla.org/en-US/security/advisories/mfsa2024-15/",
                  1,
                  cores=4,
                  outputDirectory=outputDir)
    '''
    embeddings = dict()

    for root, _, fileNames in os.walk(f"{outputDir}/text/"):
        for fileName in fileNames:
            with open(f'{root}/{fileName}', 'r', encoding="utf8") as file:
                # chunk the contents of the file
                embeddings.update(await embed.createEmbedding(file.read()))

            os.remove(f'{root}/{fileName}')

    if len(embeddings) > 0:
        db.saveToDB(embeddings, collectionName)

    promptEmbedding = list((await embed.createEmbedding(prompt, maxChunkSize=sys.maxsize,
                                                 chunkOverlap=0,
                                                 delimiter="\n"*50)).values())[0]
    hydeResponse = model.hydePrompt(prompt)
    hydeEmbedding = list((await embed.createEmbedding(hydeResponse, maxChunkSize=sys.maxsize,
                                                 chunkOverlap=0,
                                                 delimiter="\n"*50)).values())[0]

    promptResults = db.queryDB(promptEmbedding, collectionNames=[collectionName], maxHits=50)
    promptResponse = model.prompt(promptResults, prompt)
    hydeResults = db.queryDB(hydeEmbedding, collectionNames=[collectionName], maxHits=50)
    hydeResponse = model.prompt(hydeResults, prompt)

    print(f"Prompt Response:\n{promptResponse}\nHyde Response:\n{hydeResponse}")
    print(f"Time: {perf_counter() - start}")

if __name__ == "__main__":
    # Async is currently bugged on windows platforms of the current version.  This workaround changes to selecter event loop
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(run(QDrantVectorDB("129.21.21.11"),
                    OpenAIEmbed("text-embedding-3-small"),
                    GPT("You are an advanced subject matter expert on the field of cybersecurity", "gpt-4-turbo-preview"),
                    Crawler))
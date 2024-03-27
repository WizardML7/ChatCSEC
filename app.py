from database.DBInterface import iDB
from database.QDrantDB import QDrantDB
from embed.embedInterface import iEmbed
from embed.openAIEmbed import OpenAIEmbed
from model.modelInterface import iModel
from model.GPT import GPT
from scraper.iCrawler import ICrawler
from scraper.crawler import Crawler

import os
import sys

def run(db: iDB, embed: iEmbed, model: iModel, crawler: ICrawler):
    prompt = "Which CVEs are in the mozilla foundation 2024-15 security advisory?"


    db.createCollection("InitialTesting", 1536)

    outputDir = "./data/"
    crawler.crawl("https://www.mozilla.org/en-US/security/advisories/mfsa2024-15/",
                  0,
                  cores=4,
                  outputDirectory=outputDir)

    embeddings = dict()

    for root, _, fileNames in os.walk(f"{outputDir}/text/"):
        for fileName in fileNames:
            with open(f'{root}/{fileName}', 'r', encoding="utf8") as file:
                # chunk the contents of the file
                embeddings.update(embed.createEmbedding(file.read()))

            os.remove(f'{root}/{fileName}')

    db.saveToDB(embeddings, "InitialTesting")

    # TODO: Fix this.  Soon.
    results = db.queryDB(list(embed.createEmbedding(prompt, maxChunkSize=sys.maxsize, chunkOverlap=0, delimiter="\n"*50).values())[0], collectionNames=["InitialTesting"])
    response = model.prompt(results, prompt)

    print(response)

if __name__ == "__main__":
    run(QDrantDB("129.21.21.11"),
        OpenAIEmbed,
        GPT("You are an advanced subject matter expert on the field of cybersecurity", "gpt-4-turbo-preview"),
        Crawler)
from database.DBInterface import iDB
from database.QDrantDB import QDrantDB
from embed.embedInterface import iEmbed
from embed.embedPrepper import EmbedPrepper
from embed.openAIEmbed import OpenAIEmbed
from model.modelInterface import iModel
from model.GPT import GPT
from scraper.iCrawler import ICrawler
from scraper.crawler import Crawler

import os

def run(db: iDB, embed: iEmbed, model: iModel, crawler: ICrawler):
    prompt = "What is NIST and why is it important?"

    db.createCollection("ChatCSEC", 1536)

    outputDir = "./data/"
    crawler.crawl("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-28.pdf",
                  1,
                  baseDirectory=["https://doi.org", "https://nvlpubs.nist.gov"],
                  cores=4,
                  outputDirectory=outputDir)

    embeddings = dict()

    for _, dir, fileNames in os.walk(f"{outputDir}/text/"):
        for fileName in fileNames:
            with open(f'{outputDir}/{dir}/{fileName}', 'r') as file:
                # chunk the contents of the file
                content = EmbedPrepper.chunkTextBySize(file.read())

                embeddings.update(embed.createEmbedding(content))

    db.saveToDB(embeddings,"ChatCSEC")

    results = db.queryDB(prompt)
    response = model.prompt(results, prompt)

    print(response)

if __name__ == "__main__":
    run(QDrantDB(""),
        OpenAIEmbed,
        GPT("You are an advanced subject matter expert on the field of cybersecurity", "gpt-3.5-turbo"),
        Crawler)
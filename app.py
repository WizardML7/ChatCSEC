from database import QDrantDB
from database.QDrantDB import iDB
from embed.embedPrepper import EmbedPrepper
from embed.openAIEmbed import OpenAIEmbed, iEmbed
from model import GPT
from model.GPT import iModel
from scraper.crawler import Crawler, ICrawler
import os

if __name__ == "__main__":

    os.environ["OPENAI_API_KEY"] = ""

    chatbot = GPT("You are an advanced subject matter expert on the field of cybersecurity", "gpt-3.5-turbo")
    the_database = QDrantDB()
    the_prepper = EmbedPrepper()
    the_embed = OpenAIEmbed()
    the_crawler = Crawler()

    the_database.createCollection("ChatCSEC", 100)


    temp = the_prepper.chunkTextBySize(the_crawler.crawl("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-28.pdf", 1, baseDirectory=["https://doi.org", "https://nvlpubs.nist.gov"], cores=4))

    embeddings = the_embed.createEmbedding(the_prepper.removeExtraWhitespace(temp))

    for i,v in embeddings:
        print(f"key:{i}")
        print(f"value: {v}")

    the_database.saveToDB(embeddings,"ChatCSEC")

    prompt = "What is NIST and why is it important?"

    results = the_database.queryDB(prompt,"ChatCSEC")

    response = chatbot.prompt(results,prompt)

    print(response)



    pass
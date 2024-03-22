from database.QDrantDB import QDrantDB
from embed.embedPrepper import EmbedPrepper
from embed.openAIEmbed import OpenAIEmbed
from model.GPT import GPT
from scraper.crawler import Crawler
import os

if __name__ == "__main__":

    os.environ["OPENAI_API_KEY"] = ""

    chatbot = GPT("You are an advanced subject matter expert on the field of cybersecurity", "gpt-3.5-turbo")
    the_database = QDrantDB("")
    the_prepper = EmbedPrepper()
    the_embed = OpenAIEmbed()
    the_crawler = Crawler()

    the_database.createCollection("ChatCSEC", 1536)

    #TODO:Make this crawler output actually work
    #makes a folder of files
    the_crawler.crawl("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-28.pdf", 1, baseDirectory=["https://doi.org", "https://nvlpubs.nist.gov"], cores=4)

    #temp = the_prepper.chunkTextBySize(the_crawler.crawl("https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-28.pdf", 1, baseDirectory=["https://doi.org", "https://nvlpubs.nist.gov"], cores=4))

    the_string = ""
    for i in os.walk("scraper/text"):
        i = the_prepper.chunkTextBySize(i)
        i = the_prepper.removeExtraWhitespace(i)
        the_string += i

    embeddings = the_embed.createEmbedding(i)

    for i,v in embeddings:
        print(f"key:{i}")
        print(f"value: {v}")

    the_database.saveToDB(embeddings,"ChatCSEC")

    prompt = "What is NIST and why is it important?"

    results = the_database.queryDB(prompt,"ChatCSEC")

    response = chatbot.prompt(results,prompt)

    print(response)



    pass

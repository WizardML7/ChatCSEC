# ChatCSECv0.2
A Cybersecurity Expert AI application leveraging OpenAI's GPT model to provide improved, accurate responses to cybersecurity queries. Additionally, ChatCSEC offers a configurable system for training a chatbot to work with internal or private documents.
<br>
The project was authored by Domenic Lo Iacono, Kyri Lea, Brian McNulty, and Rich Kleinhenz. 

## Description
The ChatCSEC application contains the following components:
- User Interface
- Model
- Embedding Model
- Vector Database Connection
- Web Scraper
<br>
The application is designed to be modular, and each component can be substituted to use another model, embedding model, database, or web scraper. 

### User Interface
This is how users will interact with the application

### Model
ChatCSEC is developed using OpenAI's `gpt-4-0125-preview` model, which is the most recent iteration of the generative pre-trained transformer (GPT) large language models released by OpenAI. This family of models uses the transformer architecture and is trained on large, unlabeled sets of text data to understand and produce natural language, images, and code. When augmented by the industry-specific knowledge provided through embedding, ChatCSEC leverages the underlaying model to formulate answers to cybersecurity-specific queries.
<br>
Requires an OpenAI API key for the model specified. 

### Embedding Model
Embedding is a method for modifying the way a model responds by providing information it was not originally trained on. Inputs such as words, sentences, or code are broken into tokens that are then represented numerically so the model can understand the symantic relationships between them. 
<br>
ChatCSEC uses the `text-embedding-3-small` model from OpenAI to process documents and other text fed to it. Any newly created embeddings will be integrated into the vector database and together provide the foundational cybersecurity knowledge that powers the chatbot.
<br>
Requires an OpenAI API key for the model specified.

### Vector Database
A vector database is used for the rapid storage and retrieval of datapoints used by the LLM. Data from the embedding model is passed to the database for storage so information used to train the model is retained between uses. ChatCSEC uses QDrant as its vector database. Setting up the database to contain the embeddings is a prerequisite of the project. 

### Web Scraper
Keeping the model up to date with the latest information can be a time-consuming task, and the web scraper automates that process. Simply feed it a URL to crawl for content and it will embed the information on that page, as well as following links to a specified depth to gather all content from a site. Can be used with regular expressions to match a certain pattern, such as obtainining a certain type of security report from a site. 

## Installation for Developers

## Usage

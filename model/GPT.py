from .modelInterface import iModel
from openai import OpenAI
from os import environ
class GPT(iModel):
    """
    Implementation of OpenAI's ChatGPT model.  Requires the environment variable "OPENAI_API_KEY" to be set.
    """
    def __init__(self, systemMessage: str, model: str):
        """
        Creates a client to communicate with the OpenAI API using the environment variable API key.

        Args:
            systemMessage (str): The system message to provide to the completions model.
            model (str):  The model identifier for the client to use.  A current list can be
                found at https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo.
        """
        self.client = OpenAI(api_key=environ["OPENAI_API_KEY"])
        self.model = model
        self.messages = [
            {"role": "system", "content": systemMessage}
        ]

    def prompt(self, context: str, prompt: str) -> str:
        """
        Method to prompt the language model with a statement or question, while providing context for
        improved responses.

        Args:
            context (str): A section of text that the model may find useful to more adequately respond to the prompt.
            prompt (str): A string to ask the language model with.

        Returns:
            None

        TODO:
            Remove context from past user prompts to save on token space.
        """
        self.messages.append({"role": "user",
                              "content": f"CONTEXT:\n"
                                         f"{context}\n"
                                         f"QUESTION:\n"
                                         f"{prompt}\n"
                                         f"INSTRUCTIONS:\n"
                                         f"The CONTEXT above are snippets of similar text towards the users question.\n"
                                         f"Answer the users QUESTION using the CONTEXT text above.\n"
                                         f"Keep your answer ground in the facts of the DOCUMENT.\n"
                                         f"If the CONTEXT doesn’t contain the facts to answer the QUESTION then try to answer without the CONTEXT\n"
                                         f"Explicitly say at the end of your statement whether the context was used to make your answer"}
                             )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

        return response.choices[0].message.content

    def hydePrompt(self, prompt: str) -> str:
        """
        Creates a hypothetical answer to a prompt.  This answer can be used to gain more relavance
        during semantic searches.

        Notes:
            The model is instructed to create a hypothetical and fake answer, this answer should not be provided to the
            user, however should be embedded and used to search the vector database.  Research HyDE (Hypothetical
            Document Embedding) for more information

        Args:
            prompt (str): A question for the model to make a hypothetical response to.

        Returns:
            str: A hypothetical answer to the prompt provided
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are used to create hypothetical documents for hypothetical document embedding.  Ensure that your responses will have enough relevance to the probable answer that it will retrieve the proper documents from a similarity search."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content


def testGPT():
    model = GPT("You are an advanced subject matter expert on the field of cybersecurity", "gpt-3.5-turbo")
    response = model.prompt("A new vulnerability was found in the Google search engine with a CVSS score of 10. The vulnerability was found on March 16th, 2024. The vulnerability is known as 'Vendetta'",
                            "What is the most recent vulnearbility found in the google search engine with a cvss score of 10?")
    print(response)
    response = model.prompt("A new vulnerability was found in the Google search engine with a CVSS score of 10. The vulnerability was found on March 16th, 2024. The vulnerability is known as 'Vendetta'",
                            "Who was the 45th president of the United States?")
    print(response)

if __name__ == "__main__":
    testGPT()
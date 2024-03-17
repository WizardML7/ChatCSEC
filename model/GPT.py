from modelInterface import iModel
from openai import OpenAI
from os import environ
class GPT(iModel):
    def __init__(self, systemMessage: str, model: str):
        self.client = OpenAI(api_key=environ["OPENAI_API_KEY"])
        self.model = model
        self.messages = [
            {"role": "system", "content": systemMessage}
        ]

    def prompt(self, context: str, prompt: str) -> str:
        # May be able to remove context and instruction section for prompts that come after to save tokens
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
                                         f"Make note of whether your answer came from the context or not"}
                             )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

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
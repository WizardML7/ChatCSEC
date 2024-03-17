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

    def prompt(self, system: str, context: str, prompt: str) -> str:
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
                                         f"If the CONTEXT doesn’t contain the facts to answer the QUESTION then try to answer without the CONTEXT"}
                             )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

        return response.choices[0].message.content


from abc import ABC, abstractmethod

class iModel(ABC):
    """
    A generic interface used for language models to support dependency injection, inversion, and polymorphism in the
    main application.  All models should conform to this interface to make sure comparisons between components can be
    as simple and accurate as possible.
    """
    @abstractmethod
    def prompt(self, context: str, prompt: str) -> str:
        """
        Method to prompt the language model with a statement or question, while providing context for
        improved responses.

        Args:
            context (str): A section of text that the model may find useful to more adequately respond to the prompt.
            prompt (str): A string to ask the language model with.

        Returns:
            str: The models response to the prompt
        """
        pass

    @abstractmethod
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
        pass
from langchain_core.documents import Document
from openai import OpenAI
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from transformers import GPTNeoXForCausalLM, AutoTokenizer

class AbstractModel(ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def generate(self, sentences, query):
        pass

    @abstractmethod
    def prompting(self, sentences, query):
        pass


class OpenAIModel(AbstractModel):
    def __init__(self, model_name):
        super().__init__(model_name)
        load_dotenv()
        model = OpenAI()

    def generate(self, sentences, query):
        prompt = self.prompting(sentences, query)
        completion = self.model.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "Combine only Context section provided and answer based on it only, summerizer it and dont use of your knowlegde in answer."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

    def prompting(self, sentences, query):
        sentences = [sentence.page_content if isinstance(sentence, Document) else sentence for sentence in sentences]
        prompt = f"""
        Answer the request only using the below senteces.
        senteces:
        
        {"              ".join(sentences)}

        Request: {query}"""
        return prompt


class Pythia_1B(AbstractModel):
    def __init__(self):
        super().__init__("pythia-1b")
        self.model = GPTNeoXForCausalLM.from_pretrained(
            "EleutherAI/pythia-70m-deduped",
            revision="step3000",
            cache_dir="./pythia-70m-deduped/step3000",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "EleutherAI/pythia-70m-deduped",
            revision="step3000",
            cache_dir="./pythia-70m-deduped/step3000",
        )

    def generate(self, sentences, query):
        prompt = self.prompting(sentences, query)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        tokens = self.model.generate(**inputs)
        return self.tokenizer.decode(tokens[0])

    def prompting(self, sentences, query):
        sentences = [sentence.page_content if isinstance(sentence, Document) else sentence for sentence in sentences]
        user_prompt = f"""
        Answer the request only using the below senteces.
        senteces:
        
        {"              ".join(sentences)}

        Request: {query}"""

        prompt = f"""
        System
        Combine only Context section provided and answer based on it only, summerizer it and dont use of your knowlegde in answer.
        
        User
        {user_prompt}

        Assistant
        """
        return prompt


if __name__ == "__main__":
    model = Pythia_1B()
    print(model.generate(["this is a test"], "answer to test, how many time you take too long to respond?"))

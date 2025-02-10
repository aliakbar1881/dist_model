from langchain_core.documents import Document
from openai import OpenAI
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

class AbstractGenerator(ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def generate(self, sentences, query):
        pass

    @abstractmethod
    def prompting(self, sentences, query):
        pass


class OpenAIGenerator(AbstractGenerator):
    def __init__(self, model_name):
        super().__init__(model_name)
        load_dotenv()
        self.model = OpenAI()

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


class QwenGenerator(AbstractGenerator):
    def __init__(self):
        super().__init__("pythia-1b")
        model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate(self, sentences, query):
        prompt = self.prompting(sentences, query)
        inputs = self.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([inputs], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(**inputs, max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    def prompting(self, sentences, query):
        sentences = [sentence.page_content if isinstance(sentence, Document) else sentence for sentence in sentences]
        user_prompt = f"""
        Answer the request only using the below senteces.
        senteces:
        
        {"              ".join(sentences)}

        Request: {query}"""

        prompt = [
            {"role": "system", "content": "Combine only Context section provided and answer based on it only, summerizer it and dont use of your knowlegde in answer."},
            {"role": "user", "content": user_prompt}
        ]
        return prompt


if __name__ == "__main__":
    model = QwenGenerator()
    print(model.generate(["this is a test"], "Answer to test, how many time you take too long to respond?"))

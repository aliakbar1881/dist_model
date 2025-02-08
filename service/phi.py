import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def query_phi(prompt):
    torch.random.manual_seed(0)
    model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        torch_dtype="auto", 
        trust_remote_code=True, 
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": f"{prompt}"},
    ]

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        "temperature": 0.0,
        "do_sample": False
    }

    output = pipe(messages, **generation_args)
    return output[0]['generated_text']


if __name__ == "__main__":
    print(query_phi("how are you?"))
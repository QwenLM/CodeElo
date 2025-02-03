from openai import OpenAI


openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def get_response(prompt, model):
    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        stop=["<|eot_id|>", "\n\n---", "\n\n\n", "\n---", "---", '<|im_end|>'],
        max_tokens=4096,
        top_p=0.8,
        temperature=0.7,
        extra_body={
            'repetition_penalty': 1.1,
            'top_k': 20,
        }
    )
    response = chat_response.choices[0].message.content
    return response


if __name__ == '__main__':
    print(get_response('Hello, who are you?', "Qwen/Qwen2.5-Coder-7B-Instruct"))

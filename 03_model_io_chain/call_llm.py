from openai import OpenAI
import os
def call_chat_completions_api():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":"你好"}
        ],
    )
    print(response.choices[0].message.content)

def call_responses_api():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.responses.create(
        model="gpt-4o-mini",
        input="中国国内今天发生了哪些大事儿？",
        tools=[{"type":"web_search"}]
    )
    print(response.output_text)

call_responses_api()

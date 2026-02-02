from langchain_ollama import ChatOllama

llm=ChatOllama(model="qwen3")
response = llm.invoke("你好")
print(response.content)
from langchain.agents.middleware import ModelRetryMiddleware

# 1、定义一个ModelRetryMiddleware
middleware = ModelRetryMiddleware(max_retries=3)

# 2、创建一个agent
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini"),
    middleware=[middleware],
)

res = agent.invoke({"messages": [{"role": "user", "content": "帮我查下北京的天气"}]})
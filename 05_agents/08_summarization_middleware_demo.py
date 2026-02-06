# 1、从langchain引入自带的消息摘要中间件
from langchain.agents.middleware import SummarizationMiddleware
from langchain_ollama import ChatOllama

summarization_llm = ChatOllama(model="qwen3")

# 2、构造一个SummarizationMiddleware实例
summarization_middleware = SummarizationMiddleware(
    model=summarization_llm,
    # 可以传三种不同的触发条件：
    # token达到多少后做摘要：("tokens",200),
    # messages_list当中的消息数量达到多少后做摘要：("messages",20)
    # 当前token总数达到了模型最大能支持的上下文长度的比例的多少，开始做摘要：("fraction",0.5)
    trigger=("tokens",200),
    keep=("messages",3)
)

# 3、构建agent，传入summarization_middleware
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(
    model=llm, # 推理模型使用更大的大模型
    middleware=[summarization_middleware],
    checkpointer=checkpointer
)

# 第一次调用
res = agent.invoke({"messages": [{"role": "user", "content": "什么是langchain"}]},config={"configurable":{"thread_id":"1"}})
print('第一次调用的结果：',res['messages'])
print('='*50)

# 第二次调用
res = agent.invoke({"messages": [{"role": "user", "content": "什么是langgraph"}]},config={"configurable":{"thread_id":"1"}})
print('第二次调用的结果：',res['messages'])
print('='*50)
# 第三次调用
res = agent.invoke({"messages": [{"role": "user", "content": "什么是python的协程"}]},config={"configurable":{"thread_id":"1"}})
print('第三次调用的结果：',res['messages'])
print('='*50)

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm
)
def no_memory_agent():

    agent = create_agent(
    model=llm
    )
    # 1、第一次调用
    res = agent.invoke({"messages": [{"role": "user", "content": "什么是langchain"}]})
    print('第一次调用',res['messages'])

    # 2、第二次调用
    res = agent.invoke({"messages": [{"role": "user", "content": "我刚才问你什么了"}]})
    print('第二次调用',res['messages'])

def memory_agent():

    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.checkpoint.base import BaseCheckpointSaver
    import sqlite3
    # 1、使用InMemorySaver
    checkpointer = InMemorySaver()

    # 2、使用SqliteSaver
    sqlite_saver = SqliteSaver(conn=sqlite3.connect("./agent_memory.db",check_same_thread=False))


    agent = create_agent(
        model=llm,
        checkpointer=sqlite_saver
    )

    # 1、第一次调用:传入thread_id，不同thread_id代表的是不同的消息列表/上下文
    # res = agent.invoke({"messages": [{"role": "user", "content": "什么是langchain"}]},config={"configurable":{"thread_id":"1"}})
    # print('第一次调用',res['messages'])

    # 2、第二次调用：传入和第一次调用相同的thread_id，代表使用上一次调用的 消息列表/上下文
    res = agent.invoke({"messages": [{"role": "user", "content": "我刚才问你什么了"}]},config={"configurable":{"thread_id":"1"}})
    print('第二次调用',res['messages'])

memory_agent()

def init_chat_model_demo():

    from langchain.chat_models import init_chat_model
    import os

    llm_model = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
        base_url = os.getenv("OPENAI_BASE_URL"),
        api_key = os.getenv("OPENAI_API_KEY"),
    )

    resposne = llm_model.invoke("什么是langchain")
    print(resposne.content)

def from_chat_model_package_demo():

    from langchain_openai import ChatOpenAI

    llm_model = ChatOpenAI(model="gpt-4o-mini",)
    resposne = llm_model.invoke("什么是langchain")
    print(type(resposne))
    print(resposne.content)

def message_demo():
    from langchain_openai import ChatOpenAI
    from langchain.messages import AIMessage,HumanMessage,SystemMessage
    llm_model = ChatOpenAI(model="gpt-4o-mini",)

    # 使用message class 构造message 实例
    messages_list=[
        SystemMessage(content="你是一个专业的翻译"),
        HumanMessage(content="你能为我做什么"),
    ]

    # 2. 使用message class 构造message 实例
    messages_list=[
        ("system","你是一个专业的翻译"),
        ("human","你能为我做什么"),
    ]

    response = llm_model.invoke(messages_list)

    print(type(response))
    print(response.content)

async def call_llm_async_demo():

    from langchain_openai import ChatOpenAI
    from langchain.messages import AIMessage,HumanMessage,SystemMessage
    llm_model = ChatOpenAI(model="gpt-4o-mini",)

    # 使用message class 构造message 实例
    messages_list=[
        SystemMessage(content="你是一个专业的翻译"),
        HumanMessage(content="你能为我做什么"),
    ]
    # 事件循环：EventLoop
    response = await llm_model.ainvoke(messages_list)
    print(response.content)

def call_llm_streaming_demo():

    from langchain_openai import ChatOpenAI
    from langchain.messages import AIMessage,HumanMessage,SystemMessage
    llm_model = ChatOpenAI(model="gpt-4o-mini",)
    import logging
    logging.basicConfig(level=logging.DEBUG)

    # 使用message class 构造message 实例
    messages_list=[
        HumanMessage(content="帮我解释一下什么是费马大定理，帮我证明一下"),
    ]
    import time
    # model.stream()得到一个迭代器对象，需要通过for循环去迭代该对象，并获取到其内部的chunk
    for chunk in llm_model.stream(messages_list):
        # 得到的对象是AIMessageChunk
        print(chunk.content,end="")
        time.sleep(0.2)

def call_llm_batch_demo():

    from langchain_openai import ChatOpenAI
    from langchain.messages import AIMessage,HumanMessage,SystemMessage
    llm_model = ChatOpenAI(model="gpt-4o-mini",)

    # 使用message class 构造message 实例
    messages_list=[
        HumanMessage(content="解释下什么是langchain"),
    ]
    messages_list2=[
        HumanMessage(content="解释下langchain的价值是什么"),
    ]
    batch_response = llm_model.batch([messages_list,messages_list2])

    for single_response in batch_response:
        print(single_response.content)



if __name__ == "__main__":
    call_llm_batch_demo()


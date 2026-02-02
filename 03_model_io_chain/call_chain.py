def runnable_sequence():
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from pydantic import BaseModel
    class CalendarEvent(BaseModel):
            name: str
            date: str
            participants: list[str]

    template = ChatPromptTemplate.from_messages(
        messages=[("user","{input_question}")]
    )

    llm = ChatOpenAI(model="gpt-4o-mini")
    new_llm = llm.with_structured_output(schema=CalendarEvent)

    # 通过管道符，组装成chain对象 
    # python的魔法方法：__add__ : 实现了 + 的操作, __or__: 实现了 | 的操作，__enter__ __exit__
    chain = template | new_llm
    res=chain.invoke({"input_question":"我要在2026年2月12日组织一个会议，邀请张三和李四参加,名字叫做：“会议A”"})
    print(res)

def runnable_parallel():
    
    from langchain.chat_models import init_chat_model
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableParallel
    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )

    # StrOutputParser: 把llm.invoke得到的AIMesssage对象，提取出content内容
    english_chain = (
        PromptTemplate.from_template("把这个句子{topic}翻译成英文") | llm | StrOutputParser()
    )
    

    korean_chain = (
        PromptTemplate.from_template("把这个句子{topic}翻译成韩文") | llm | StrOutputParser()
    )

    # 构建一个RunnableParallel的实例对象
    parallel_instance = RunnableParallel(
         english_output = english_chain,
         korean_output = korean_chain,
    )

    res = parallel_instance.invoke({"topic":"你好"})

    print(res)

runnable_parallel()

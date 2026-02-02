def use_prompt_demo():

    # 0、导包

    # 1、定义JSON结构:使用pydantic定义数据结构
    # 所希望的JSON结构 schema ：{"prime":[1,2,3],"count":[0,1,2]}
    from pydantic import BaseModel, Field
    class Prime(BaseModel):
        prime: list[int] = Field(description="素数")
        count: list[int] = Field(description="小于该素数的素数个数")

    # 2、引入langchain的JsonOutputParser
    from langchain_core.output_parsers import JsonOutputParser

    # 3、创建JsonOutputParser实例
    parser = JsonOutputParser(pydantic_object=Prime)

    # 4、调用大模型，在system message当中添加格式化指令
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(
        [("system",parser.get_format_instructions()),("user","任意生成5个1000-100000之间素数，并标出小于该素数的素数个数")]
    )


    # 得到json字符串
    print(response.content) 

    # 通过调用json_parser的invoke方法，将AIMessage转换为Python dict
    res = parser.invoke(response)
    print(type(res))
    print(res['prime'])

def use_model_structured_output_demo():
    from openai import OpenAI
    from pydantic import BaseModel
    import logging
    # 查看底层调用API日志
    logging.basicConfig(level=logging.DEBUG)
    # 1、JSON Schema
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    client = OpenAI()

    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":"2026年2月15号，张三和李四会举行一个会议，名字为：“公司会议”"}],
        response_format=CalendarEvent
    )

    print(response.choices[0].message.parsed)
    print(type(response.choices[0].message.parsed))

def use_model_structured_output_langchain_demo():
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel
    import logging
    import os
    # 查看底层调用API日志
    logging.basicConfig(level=logging.DEBUG)
    #1、构造LLM对象
    # llm = ChatOpenAI(model="gpt-4o-mini")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",
                                 base_url='https://api.openai-proxy.org/google',
                                 api_key=os.getenv("OPENAI_API_KEY"))

    #2、构造schema结构
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    # 3、调用llm的统一方法：with_structured_output()，得到新的LLM对象，
    new_llm = llm.with_structured_output(schema=CalendarEvent)

    # 4、通过新的LLM对象invoke，就能获取结构化结果
    res = new_llm.invoke([{"role":"user","content":"2026年2月15号，张三和李四会举行一个会议，名字为：“公司会议”"}])

    print(type(res))
    print(res)

use_model_structured_output_langchain_demo()


import langchain_core.output_parsers
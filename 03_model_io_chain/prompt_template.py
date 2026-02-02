from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "你是一个专业的翻译"),
        ('user',"请把这句话翻译成{sentence}英文")
    ]
)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
llm.abatch
response = llm.invoke(template.invoke({'sentence':"今天天气很好"}))
print(response.content)
llm.abatch
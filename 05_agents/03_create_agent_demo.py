from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
from langchain.messages import AIMessageChunk,ToolMessage

load_dotenv()
# 1、构造一个agent实例

# 1.1 定义一个模型
llm = ChatOpenAI(model="gpt-4o-mini")

# 1.2 定义模型能使用的工具
@tool
def get_weather(city:str,date:str):
    """
    获取城市在特定日期的天气
    """
    return f'在{city} {date}的天气是晴朗的'

agent = create_agent(
    model=llm,
    tools=[get_weather]
)

# 2. 调用agent，获取结果
# res = agent.invoke({"messages":[{"role":"user","content":"北京在2023-12-25的天气是多少？"}]})
# # 得到的结果为一个Dict，包含messages键，需要从messages键当中取出结果，
# # 这个结果就是messages_list, 取最后一个message，这个message就是AIMessage，从中取出content
# print(res["messages"][-1].content)

# 3. 通过流式调用agent：stream_mode参数填充为messages，可以流式输出ToolMessage和AIMessageChunk
for chunk in agent.stream({"messages":[{"role":"user","content":"北京在2023-12-25的天气是多少？告诉我适合去哪里玩，以及我需要注意的事项是什么？"}]},stream_mode="messages"):
    if type(chunk[0]) == ToolMessage:
        continue
    print(chunk[0])
    print("="*50)

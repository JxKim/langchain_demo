from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool


# 1、定义一些工具
# 1.1 工具一

@tool(description="获取城市的天气")
def get_weather(city: str) -> str:
    return f"{city}的天气是晴朗的"

@tool(description="转账金额到指定人")
def transfer_money(amount:float,to:str)->str:
    return f"成功转账{amount}元到{to}"

# 2、定义一个HumanInTheLoopMiddleware
human_in_the_loop_middleware = HumanInTheLoopMiddleware(interrupt_on={"get_weather":False,"transfer_money":True})

# 3、创建一个agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini"),
    tools=[get_weather,transfer_money],
    middleware=[human_in_the_loop_middleware],
    checkpointer=InMemorySaver(),
    system_prompt="你是一个智能助手，需要根据用户指令完成问题"
)

# 4、调用agent

# 4.1 让agent调用get_weather工具
res = agent.invoke({"messages": [{"role": "user", "content": "帮我查下北京的天气"}]},config={"configurable":{"thread_id":1}})
print(res)
print("="*50)

# 4.3 让agent调用transfer_money工具
res = agent.invoke({"messages": [{"role": "user", "content": "帮我转账1000元到张三"}]},config={"configurable":{"thread_id":1}})
print(res)
print("="*50)

# 5、解析__interrupt__的内容
interrupt_list = res["__interrupt__"]
interrupt = interrupt_list[0]
# 获取到模型调用工具的参数和工具名称
interrupt_tool_args = interrupt.value["action_requests"][0]["args"] 
interrupt_tool_name = interrupt.value["action_requests"][0]["name"] 
print('工具参数为',interrupt_tool_args)
print('工具名称为',interrupt_tool_name)
# review_tool_call(interrupt_tool_name,interrupt_tool_args) 可以写一个参数对调用的工具的参数进行一个审核

# 审核完成，让工具调用继续执行下去
from langgraph.types import Command
decision={"type":"edit","edited_action":{"name":"transfer_money","args":{"amount":500,"to":"张三"}}}
res = agent.invoke(Command(resume={"decisions":[decision]}),config={"configurable":{"thread_id":1}})

print(res)
from langchain.tools import tool
from pydantic import BaseModel,Field
from langchain_core.messages import AIMessage,ToolMessage,HumanMessage
class GetWeatherArgs(BaseModel):
    city: str = Field(description="城市名称, 比方说 北京市， 武汉市，需要传递城市的全名")
    date : str = Field(description="天气日期，格式是yyyy-MM-dd")


@tool(description="获取城市在特定日期的天气",args_schema=GetWeatherArgs)
def get_weather(city:str,date:str):
    return f'城市{city}在{date}的天气是晴朗的'


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini",)

# 在模型上绑定工具，得到的新的llm模型，后续在调用open ai 接口时，会自动传递tools参数
llm_with_tools = llm.bind_tools([get_weather])

human_message =HumanMessage(content="北京在2023-12-25的天气是多少？")
res = llm_with_tools.invoke([human_message])
ai_message = res 
tool_id = res.tool_calls[0]['id']
print(res)

# 2、解析 AIMessage，具体调用get_weather工具
tool_call = res.tool_calls[0]['args']
tool_res = get_weather.invoke(tool_call)

# 3、封装Tool Message
tool_message = ToolMessage(tool_call_id=tool_id,content=tool_res)

llm_second_res = llm_with_tools.invoke([human_message,ai_message,tool_message])

print('模型第二次的回复结果为',llm_second_res)
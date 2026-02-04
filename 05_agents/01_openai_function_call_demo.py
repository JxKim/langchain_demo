from openai import OpenAI

# 1、定义一个工具/function

def get_weather(city:str,date:str):
    try:
        return f'城市{city}在{date}的天气是晴朗的'
    except Exception as e:
        return '工具调用失败'

# 2、构建function的 json schema
get_weather_function_schema= {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市在特定日期的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称, e.g. San Francisco",
                    },
                    "date" :{
                        "type":"string",
                        "description":"想要查询的天气的日期, e.g. 2023-12-25"
                    }
                },
                "required": ["city","date"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }


# 3、调用OpenAI API，传入大模型能够使用的工具的 schema信息
client = OpenAI()
message_list = [
        {"role": "user", "content": "北京在2023-12-25的天气是多少？"}
    ] 
response = client.chat.completions.create(
    model="gpt-4o-mini",
    tools=[get_weather_function_schema],
    messages=message_list
)

print(response.choices[0].message)

message_list.append(response.choices[0].message)
# 4、解析OpenAI API返回的结果，具体调用get_weather函数
too_call_arguments = response.choices[0].message.tool_calls[0].function.arguments
tool_call_id = response.choices[0].message.tool_calls[0].id
# 构建一个tool message
import json 
# 将json字符串解析成dict，获取到每个参数值，并具体调用，得到结果，封装成一个tool message 
import json
parameter_dict = json.loads(too_call_arguments)
city = parameter_dict["city"]
date = parameter_dict["date"]
weather = get_weather(city,date)
message_list.append(
    {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": json.dumps({"weather": weather}),
    }

)
# 5、再次调用OPENAI API ，将上面的所有信息列表，都传给OPENAI API，得到最终结果
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=message_list
)

print('大模型得到工具调用结果之后的回复',response.choices[0].message.content)
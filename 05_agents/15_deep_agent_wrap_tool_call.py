# -*- coding: utf-8 -*-
"""
DeepAgents Middleware 极简案例
核心：实现工具调用的日志监控中间件
"""
import os
import time

from langchain.agents.middleware import wrap_tool_call
from langchain.agents.middleware.types import AgentMiddleware, ToolCallRequest
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
load_dotenv(find_dotenv())


# ======================== 1. 定义测试工具 ========================
@tool
def add_numbers(a: int, b: int):
    """计算两个数字的和"""
    time.sleep(0.5)  # 模拟耗时操作
    result = a + b
    print(f"[工具执行] {a} + {b} = {result}")
    return result


@wrap_tool_call
def log_tool_call(request, handler):
    tool_name = request.tool_call["name"]
    tool_args = request.tool_call["args"]

    # 1. 前置逻辑
    print(f"\n[前置中间件] 工具调用开始 - 工具名: {tool_name}, 参数: {tool_args}, 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    start_time = time.time()

    # 2. 执行工具 (调用 handler)
    result = handler(request)

    end_time = time.time()
    duration = end_time - start_time

    # 3. 后置逻辑
    # 先尝试从 result 对象中获取 content 属性；如果 result 没有 content 属性（比如不是 ToolMessage 类型），就把 result 转成字符串作为兜底值。
    content = getattr(result, "content", str(result))
    print(f"[后置中间件] 工具调用完成 - 工具名: {tool_name}, 结果: {content}, 耗时: {duration:.2f}秒")

    return result

# ======================== 3. 配置Agent并绑定Middleware ========================
# 初始化LLM
llm = init_chat_model(
    model='gpt-4o-mini',
    model_provider="openai"
)

# 创建Agent，绑定中间件
deep_agent = create_deep_agent(
    model=llm,
    tools=[add_numbers],
    checkpointer=InMemorySaver(),
    # 绑定中间件：传入 Middleware 实例列表
    middleware=[log_tool_call],
    system_prompt="你是一个计算器助手，使用add_numbers工具完成加法计算，回答仅返回计算结果。"
)

# ======================== 4. 执行测试 ========================
if __name__ == "__main__":
    # 会话配置
    thread_config = {"configurable": {"thread_id": "middleware_test_1"}}

    # 调用Agent
    result = deep_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "帮我计算 100 + 200 的结果"}
            ]
        },
        config=thread_config
    )

    # 输出最终结果
    print("\n=== 最终回复 ===")
    print(result["messages"][-1].content)
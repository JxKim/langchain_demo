from langchain_mcp_adapters.client import MultiServerMCPClient


# 1、构造 LangChain MultiMcpServerClient
multi_server_client = MultiServerMCPClient(
    connections={
        "amap_map":{
      "transport": "sse",
      "url": "https://mcp.api-inference.modelscope.net/ccaef2a2308042/sse"
    },
    "12306_mcp":{
      "transport": "sse",
      "url": "https://mcp.api-inference.modelscope.net/5b6ff2cd306e4d/sse"
    }
    }
)

async def main():

    tools = await multi_server_client.get_tools()

    print(tools)

    from langchain.agents import create_agent
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini")

    agent = create_agent(
        model=llm,
        tools=tools
    )

    res = await agent.ainvoke({"messages": [{"role": "user", "content": "帮我查下2026年2月10号从北京到武汉的车票"}]})

    ai_message = res["messages"][-1].content

    print(ai_message)



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
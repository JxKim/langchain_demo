from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters

async def main():

    server_params = StdioServerParameters(
        command=r"D:\PycharmProjects\lessons\demo_class\LangChainDemo\.venv\Scripts\python.exe",
        args=[r"D:\PycharmProjects\lessons\demo_class\LangChainDemo\05_agents\04_mcp_stdio_server.py"]
    )

    async with stdio_client(server_params) as (read_stream,write_stream):
        async with ClientSession(read_stream=read_stream,write_stream=write_stream) as session:

            await session.initialize()


            tools_list = await session.list_tools()

            # 执行工具

            tool_call_result =await session.call_tool(name="get_weather",arguments={"city":"北京","date":"2023-12-12"})


            print(tools_list)

            print(tool_call_result)

            # prompt

            prompt_res = await session.list_prompts()

            print(prompt_res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


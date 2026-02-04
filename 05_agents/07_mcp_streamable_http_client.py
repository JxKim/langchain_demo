from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession

async def main():

    url = "http://localhost:8000/mcp"

    async with streamable_http_client(url=url) as (read_stream,write_stream,_):
        async with ClientSession(read_stream=read_stream,write_stream=write_stream) as session:

            # 1、初始化
            await session.initialize()

            # 2、获取到server端所有工具


            tools = await session.list_tools()

            print(tools)

            # 3、调用tool

            result = await session.call_tool(name="get_temperature",arguments={"city":"北京","date":"2023-12-12"})


            print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

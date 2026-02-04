from mcp.server import FastMCP


# 1、定义一个MCP的服务端实例
mcp = FastMCP()


@mcp.tool()
def get_weather(city:str,date:str)->str:
    return f"在{city}，{date}的天气是下雨的"

@mcp.tool()
def get_temperature(city:str,date:str)->str:
    return f"在{city}，{date}的温度是25摄氏度"


@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")


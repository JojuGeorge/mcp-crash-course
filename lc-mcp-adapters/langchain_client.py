import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI()


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "transport": "stdio",
                "args": [
                    "D:/UDEMY/LangChain/Coding/mcp-crash-course/lc-mcp-adapters/servers/math_server.py"
                ],
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    # result = await agent.ainvoke({"messages": "What is 2 + 2?"})
    result = await agent.ainvoke(
        {"messages": "What is the weather in San Francisco?"}
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
# MCP and LLM Integration with LangChain/LangGraph

## Repository Overview

The repository demonstrates how to integrate Model Context Protocol (MCP) with Large Language Models (LLMs) using LangChain and LangGraph. The primary goal is to leverage MCP to provide LLMs with access to tools and functionalities available on a remote system (in this case, a desktop commander created by Eduards https://github.com/wonderwhy-er/DesktopCommanderMCP).

## What is MCP?

Model Context Protocol (MCP) provides a standardized way for different systems or processes to communicate and control each other. It defines a set of messages and procedures for discovering, invoking, and managing tools across different environments.

### Benefits of MCP

- **Standardized Tool Access:** MCP offers a unified approach for LLMs to interact with various tools, regardless of their underlying implementation.
- **Execution:** MCP enables LLMs to execute tools on remote systems, expanding their capabilities beyond the local environment.
- **Security:** MCP can incorporate security measures for controlling tool access and preventing unauthorized operations.
- **Scalability:** MCP facilitates the integration of new tools and functionalities without requiring modifications to the LLM or its core logic.

## How MCP Works with LLMs

1. **MCP Server:** A server (e.g., `@wonderwhy-er/desktop-commander`) exposes a set of tools via MCP. It provides functionalities for interacting with the operating system.
2. **MCP Client:** The LLM interacts with the MCP server through an MCP client (`stdio_client` in `client.py`). The client manages communication and data exchange between the LLM and the server.
3. **Tool Loading:** The `load_mcp_tools` function (from `langchain_mcp_adapters.tools`) adapts the MCP tools to be compatible with LangChain/LangGraph.
4. **Agent Creation:** A LangChain/LangGraph agent is created using the LLM and the loaded tools. The agent determines which tool to use based on user input.

## Creating a Custom MCP Server

MCP servers can be created to expose custom functionalities. For example, a simple math server can be set up using the FastMCP library:

### Example: Math Server

```python
# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

In this example, the server defines two mathematical operations, `add` and `multiply`, and exposes them through the MCP interface. Running this server allows LLMs to call these functions remotely.

## Using MCP with Tool Registries

Tool registries like Smithery facilitate the management and discovery of tools available in a distributed environment. Integrating MCP with registries allows dynamic discovery of available functionalities and their seamless use in LLM workflows.

## Implementation with LangChain/LangGraph

### Connecting to the MCP Server

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@wonderwhy-er/desktop-commander"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await load_mcp_tools(session)
```

### Creating a LangGraph Agent with MCP Tools

```python
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
agent = create_react_agent(model, tools)
```

### Invoking the Agent

```python
agent_response = await agent.ainvoke({"messages": "List files in the current directory."})
```

## Main Script (`main.py`)

The following script sets up the MCP client and LangGraph agent to interact with the MCP server:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
agent = create_react_agent(model, tools)

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@wonderwhy-er/desktop-commander"],
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent_response = await agent.ainvoke({"messages": "List files in the current directory."})
            print(agent_response)

if __name__ == "__main__":
    asyncio.run(run_agent())
```

## Running the Code

To run the code, I use uv. You can run the main script with the following command:

```bash
uv run ./client.py    
```

## Conclusion

By integrating MCP with LangChain/LangGraph, we can empower LLMs to interact with system tools and perform complex tasks remotely. Creating custom MCP servers with tools like FastMCP, combined with tool registries like Smithery, enhances the flexibility and utility of LLM-based agents, making them more adaptable and powerful in diverse environments.

## Useful Resources

- https://modelcontextprotocol.io/introduction
- https://github.com/modelcontextprotocol/python-sdk
- https://smithery.ai/server/@wonderwhy-er/desktop-commander
- https://github.com/langchain-ai/langchain-mcp-adapters

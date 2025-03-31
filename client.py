# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
groq_api_key = os.environ["GROQ_API_KEY"]
google_api_key = os.environ["GOOGLE_API_KEY"]

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@wonderwhy-er/desktop-commander"],
)

# Available tools: execute_command, read_output, force_terminate, list_sessions, list_processes, kill_process, block_command, unblock_command, list_blocked_commands, read_file, read_multiple_files, write_file, create_directory, list_directory, move_file, search_files, search_code, get_file_info, list_allowed_directories, edit_block

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

# model = ChatGroq(model="llama-3.3-70b-versatile")
# model = ChatOllama(model="qwen2.5:32b")
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inawaititialize the connection
            await session.initialize()
            tools_result = await session.list_tools()
            print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")
            tools = await load_mcp_tools(session)

            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": """'C:/path/to/uv_mcp_langchain' 
                                                  Here is a code repository. First use the list_directory and after that you can check file by file, I want you to explore it thoroughly.
                                                  Finally create the documentation of this repository in markdown with code examples."""})
            return agent_response


# Run the async function
if __name__ == "__main__":
    result = asyncio.get_event_loop().run_until_complete(run_agent())
    print(result)

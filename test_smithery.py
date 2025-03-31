import smithery
import mcp
from mcp.client.websocket import websocket_client
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
smithery_api_key = os.environ["SMITHERY_API_KEY"]

# Create Smithery URL with server endpoint
url = smithery.create_smithery_url("wss://server.smithery.ai/@wonderwhy-er/desktop-commander/ws", {}) + f"&api_key={smithery_api_key}"

async def main():
    # Connect to the server using websocket client
    async with websocket_client(url) as streams:
        async with mcp.ClientSession(*streams) as session:
            # List available tools
            tools_result = await session.list_tools()
            print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")
            
            # Example: Call a tool
            result = await session.call_tool("list_processes")
            return result

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
"""Real stdio initialization, discovery and call; not just an import check."""
import asyncio
import json
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    root = Path(__file__).resolve().parents[1]
    params = StdioServerParameters(command=sys.executable, args=[str(root / "server.py")], cwd=str(root))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            assert names == {"demonstrate_modulo", "inspect_episode_plan"}, names
            result = await session.call_tool("demonstrate_modulo", {"start": 10, "steps": 5, "modulus": 12})
            assert not result.isError
            data = result.structuredContent or json.loads(result.content[0].text)
            assert data["final"]["residue"] == 3 and data["final"]["quotient"] == 1, data
            print("PASS: stdio handshake, two-tool discovery, modulo tool call")


if __name__ == "__main__":
    asyncio.run(main())

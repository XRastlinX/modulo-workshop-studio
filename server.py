"""Read-only MCP tools. No rendering, shell, Git writes or publication tool."""
from mcp.server.fastmcp import FastMCP
from studio_core import modulo_walk, check_episode_plan

mcp = FastMCP("Modulo Workshop Studio")


@mcp.tool()
def demonstrate_modulo(start: int = 10, steps: int = 5, modulus: int = 12) -> dict:
    """Inspect a bounded modulo example, retaining the integer and quotient."""
    return modulo_walk(start, steps, modulus)


@mcp.tool()
def inspect_episode_plan(plan: dict) -> dict:
    """Report missing description fields. This does not verify their truth."""
    return check_episode_plan(plan)


if __name__ == "__main__":
    mcp.run(transport="stdio")

import asyncio
from fastmcp import FastMCP
from langchain.mcp import MCPAdapter

# 1. Initialize a simple FastMCP server
mcp = FastMCP("AnnotationDemo")

# 2. Define a tool with specific MCP annotations
@mcp.tool(
    annotations={
        "read_only_hint": False,
        "destructive_hint": True,
        "idempotent_hint": False,
        "open_world_hint": True,
        "title": "Database Cleanup Tool"
    }
)
def purge_old_records(days_old: int) -> str:
    """Deletes records older than the specified number of days."""
    return f"Purged records older than {days_old} days."

async def main():
    # 3. Pass the in-memory FastMCP server instance directly to MCPAdapter
    async with MCPAdapter(mcp) as adapter:
        # Discover tools exposed by the server
        tools = await adapter.list_tools()
        
        for tool in tools:
            print(f"Tool Name: {tool.name}")
            print(f"Tool Description: {tool.description}")
            
            # 4. Extract and print the metadata/annotations passed over MCP
            metadata = tool.metadata or {}
            mcp_info = metadata.get("mcp", {})
            annotations = mcp_info.get("tool", {}).get("annotations", {})
            
            print("\nExtracted Annotations:")
            print(f"  - Title:            {annotations.get('title')}")
            print(f"  - Destructive Hint: {annotations.get('destructive_hint')}")
            print(f"  - Read-Only Hint:   {annotations.get('read_only_hint')}")
            print(f"  - Idempotent Hint:  {annotations.get('idempotent_hint')}")
            print(f"  - Open World Hint:  {annotations.get('open_world_hint')}")

if __name__ == "__main__":
    asyncio.run(main())
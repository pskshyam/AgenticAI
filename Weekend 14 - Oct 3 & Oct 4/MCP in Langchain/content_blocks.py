import asyncio
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import ToolMessage
from pathlib import Path

async def access_multimodal_tool_content(server) -> dict:
    async with MCPAdapter(server) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("gpt-5-mini", tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Take a screenshot."}]}
        )

    # An MCP result arrives as LangChain content blocks. Image and file content
    # convert into standardized `image`/`file` blocks alongside `text`.
    for message in result["messages"]:
        if not isinstance(message, ToolMessage):
            continue
        for block in message.content_blocks:
            if block["type"] == "text":
                print(f"Text: {block['text']}")
            elif block["type"] == "image":
                preview = block.get("base64", "")[:20]
                print(f"Image mime type: {block.get('mime_type')}")
                print(f"Image base64: {preview}...")

    return result

async def main():
    server = Path("image_content.py")
    await access_multimodal_tool_content(server)


if __name__ == "__main__":
    asyncio.run(main())
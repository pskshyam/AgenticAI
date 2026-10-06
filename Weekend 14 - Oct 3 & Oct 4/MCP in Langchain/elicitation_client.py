import asyncio
from pathlib import Path
from typing import Any
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

async def test_elicitation(server):
    async with MCPAdapter(server) as adapter:
        # Pass the FastMCP instance directly into the MCPAdapter    
        tools = await adapter.list_tools()

    # Create agent with checkpointer
    agent = create_agent(
        "gpt-5-mini", tools, checkpointer=InMemorySaver()
    )
    config = {"configurable": {"thread_id": "test-session"}}

    # Run 1: Initial call with missing date
    print("--- Initial Run ---")
    res = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Use the book_table tool to reserve a table for 4 people."}]},
        config,
    )

    # Safely check for interrupt before accessing '__interrupt__'
    if "__interrupt__" not in res:
        print("No interrupt occurred. Final output:")
        print(res["messages"][-1].content)
        return

    print("Interrupt captured successfully!")
    [interrupt] = res["__interrupt__"]
    [request] = interrupt.value["requests"]
    request_key = request["key"]

    # Run 2: Resume with user input
    print("\n--- Resuming Run ---")
    answer = {"action": "accept", "content": {"date": "2026-10-15"}}

    resumed = await agent.ainvoke(
        Command(resume={"responses": {request_key: answer}}), config
    )

    print("Final Output:")
    print(resumed["messages"][-1].content)


async def main():
    server = Path("elicitation_server.py")
    await test_elicitation(server)


if __name__ == "__main__":
    asyncio.run(main())
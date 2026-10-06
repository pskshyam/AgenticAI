from mcp.server.mcpserver import Context, MCPServer
from mcp.types import (
    ElicitRequest,
    ElicitRequestFormParams,
    ElicitResult,
    InputRequiredResult,
)

mcp = MCPServer("BookingServer")


@mcp.tool()
async def book_table(
    party_size: int,
    date: str | None = None,
    ctx: Context = None,
) -> str | InputRequiredResult:
    """Books a table, requesting date if not provided."""

    # Normal call where model already supplied date
    if date:
        return f"Successfully booked table for {party_size} on {date}!"

    # First MCP round: no elicitation response yet
    if ctx.input_responses is None:

        request = ElicitRequest(
            params=ElicitRequestFormParams(
                message=f"Please specify the booking date for party of {party_size}:",
                requested_schema={
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format",
                        }
                    },
                    "required": ["date"],
                },
            )
        )

        return InputRequiredResult(
            input_requests={"booking_date": request},
            request_state=f"book_table:{party_size}",
        )

    # Second MCP round: LangChain supplied the human answer
    result = ctx.input_responses.get("booking_date")

    if not isinstance(result, ElicitResult):
        return "Booking cancelled."

    if result.action != "accept":
        return "Booking cancelled."

    date = result.content["date"]

    return f"Successfully booked table for {party_size} on {date}!"


if __name__ == "__main__":
    mcp.run()
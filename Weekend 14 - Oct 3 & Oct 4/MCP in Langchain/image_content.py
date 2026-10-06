from pathlib import Path

from mcp.server import MCPServer
from mcp.server.mcpserver import Image


mcp = MCPServer("Multimodal Test Server")

IMAGE_PATH = Path(__file__).parent / "test.png"


@mcp.tool()
def take_screenshot() -> Image:
    """Take a screenshot and return it as an image."""
    return Image(path=IMAGE_PATH)

if __name__ == "__main__":
    mcp.run()

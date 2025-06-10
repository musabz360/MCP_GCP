from mcp.server.fastmcp import FastMCP
from app import getliveTemp
import os

# Initialize MCP server
mcp = FastMCP("weather-forecast-mcp")

@mcp.tool()
async def get_live_weather(latitude: float, longitude: float) -> dict:
    """
    Get live weather details for a given latitude and longitude.
    """
    result = getliveTemp(latitude, longitude)
    return result

# Get the port from the environment variable provided by Cloud Run.
# We still define it, but FastMCP.run() likely picks it up automatically when transport="http".
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    print(f"Starting FastMCP server with HTTP transport (Cloud Run will set port {PORT})...")
    mcp.run(transport="http") # <--- MODIFIED THIS LINE
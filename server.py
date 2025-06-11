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

# Get the port from the environment variable provided by Cloud Run
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    print(f"Starting FastMCP server on port {PORT}...")
    mcp.settings.port = PORT
    mcp.settings.host = "0.0.0.0"  # Required for Cloud Run to work properly
    mcp.run(transport="streamable-http")

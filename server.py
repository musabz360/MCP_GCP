from mcp.server.fastmcp import FastMCP
from app import getliveTemp
import os # Add this line

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
# Default to 8080 if the PORT environment variable is not set (e.g., for local testing).
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    # Change transport to "http" and listen on the dynamically provided PORT
    print(f"Starting FastMCP server on port {PORT} with HTTP transport...")
    mcp.run(transport="http", port=PORT)
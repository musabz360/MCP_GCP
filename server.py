from mcp.server.fastmcp import FastMCP
from app import getliveTemp

# Initialize MCP server
mcp = FastMCP("weather-forecast-mcp")

@mcp.tool()
async def get_live_weather(latitude: float, longitude: float) -> dict:
    """
    Get live weather detailes for a given latitude and longitude.
    """
    # Call the function from app.py (remove await, since getliveTemp is sync)
    result = getliveTemp(latitude, longitude)
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")
from fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo

mcp = FastMCP("Time MCP Server")

# 简单城市 -> 时区映射表
CITY_TIMEZONE_MAP = {
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "tokyo": "Asia/Tokyo",
    "new york": "America/New_York",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "los angeles": "America/Los_Angeles",
    "berlin": "Europe/Berlin",
    "singapore": "Asia/Singapore",
}


@mcp.tool
def get_local_time(city: str) -> str:
    """
    根据城市名称获取当地时间
    示例输入: "Tokyo"
    """
    city_key = city.strip().lower()

    if city_key not in CITY_TIMEZONE_MAP:
        return f"Unsupported city: {city}. Please add it to CITY_TIMEZONE_MAP."

    timezone_str = CITY_TIMEZONE_MAP[city_key]

    try:
        now = datetime.now(ZoneInfo(timezone_str))
        return now.strftime(f"%Y-%m-%d %H:%M:%S (%Z)")
    except Exception as e:
        return f"Error getting time for {city}: {str(e)}"


if __name__ == "__main__":
    mcp.run()

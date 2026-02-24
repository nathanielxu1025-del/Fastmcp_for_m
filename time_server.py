from fastmcp import FastMCP
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

# 创建 MCP 实例
mcp = FastMCP("world-time-server")

# 初始化工具
geolocator = Nominatim(user_agent="mcp-time-server")
tf = TimezoneFinder()


@mcp.tool()
def get_local_time(place_name: str) -> str:
    """
    输入地名，返回该地当前时间
    """
    try:
        # 地名转经纬度
        location = geolocator.geocode(place_name)
        if not location:

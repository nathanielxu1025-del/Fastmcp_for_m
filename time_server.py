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
            return f"未找到地点: {place_name}"

        lat, lng = location.latitude, location.longitude

        # 经纬度转时区
        timezone_str = tf.timezone_at(lat=lat, lng=lng)
        if not timezone_str:
            return f"无法确定时区: {place_name}"

        timezone = pytz.timezone(timezone_str)

        # 获取当前时间
        local_time = datetime.now(timezone)

        return (
            f"地点: {place_name}\n"
            f"时区: {timezone_str}\n"
            f"当前时间: {local_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except Exception as e:
        return f"发生错误: {str(e)}"


if __name__ == "__main__":
    mcp.run()

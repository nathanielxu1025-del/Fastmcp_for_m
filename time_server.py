from fastmcp import FastMCP
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz # 或者 from zoneinfo import ZoneInfo (Python 3.9+)

# 初始化 MCP 服务器
mcp = FastMCP("World Clock Server")

# 初始化工具 (只需初始化一次，避免重复请求)
# Nominatim 需要设置 user_agent 以遵守使用条款
geolocator = Nominatim(user_agent="fastmcp_time_tool")
tf = TimezoneFinder()

@mcp.tool
def get_local_time(location: str) -> str:
    """
    获取指定地名的当前当地时间。
    
    Args:
        location: 地名，例如 'Beijing', 'New York', 'London', 'Tokyo'。
    
    Returns:
        包含地名、时区和当地时间的字符串。
    """
    try:
        # 1. 地理编码：地名 -> 经纬度
        # timeout 设置为 5 秒，避免网络卡顿
        location_data = geolocator.geocode(location, timeout=5)
        
        if not location_data:
            return f"❌ 错误：无法找到地点 '{location}'。请检查拼写或尝试更具体的名称（如 'City, Country'）。"
        
        lat = location_data.latitude
        lon = location_data.longitude
        full_name = location_data.address # 获取标准化后的地址名称

        # 2. 时区查找：经纬度 -> 时区名称 (例如 'Asia/Shanghai')
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        
        if not timezone_str:
            return f"❌ 错误：无法确定地点 '{full_name}' ({lat}, {lon}) 的时区。"

        # 3. 时间计算
        tz = pytz.timezone(timezone_str)
        local_time = datetime.now(tz)
        
        # 格式化时间字符串
        time_str = local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        
        return f"📍 地点：{full_name}\n🕒 时区：{timezone_str}\n⏰ 当地时间：{time_str}"

    except Exception as e:
        return f"❌ 发生错误：{str(e)}"

if __name__ == "__main__":
    mcp.run()


import traceback

from config import Config
from core.utils import get_url

botarcapi_url = Config("botarcapi_url")
headers = {"User-Agent": Config('botarcapi_agent')}


async def get_userinfo(user):
    try:
        get_ = await get_url(
            f"{botarcapi_url}user/info?user={user}",
            status_code=200,
            headers=headers,
            fmt='json',
        )

        username = get_['content']['account_info']['name']
        code = get_['content']['account_info']['code']
        return username, code
    except Exception:
        traceback.print_exc()
        return False

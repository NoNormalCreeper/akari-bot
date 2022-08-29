import ujson as json

from core.utils import get_url


async def get_profile_name(userid):
    profile_url = f'http://services.cytoid.io/profile/{userid}'
    profile = json.loads(await get_url(profile_url, 200))
    if 'statusCode' in profile and profile['statusCode'] == 404:
        return False
    uid = profile['user']['uid']
    nick = profile['user']['name']
    if nick is None:
        nick = False
    return uid, nick

import ujson as json

from core.elements import FetchTarget
from database import BotDBUtil


def get_stored_list(bot: FetchTarget, name):
    get = BotDBUtil.Data(bot).get(name=name)
    return [] if get is None else json.loads(get.value)


def update_stored_list(bot: FetchTarget, name, value):
    return BotDBUtil.Data(bot).update(name=name, value=json.dumps(value))


__all__ = ['get_stored_list', 'update_stored_list']

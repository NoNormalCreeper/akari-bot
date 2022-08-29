# https://github.com/XeroAlpha/caidlist/blob/master/backend/API.md
import urllib.parse

from core.builtins.message import MessageSession
from core.component import on_command
from core.utils import get_url

api = 'https://ca.projectxero.top/idlist/search'

i = on_command('idlist')


@i.handle('<query> {查询MCBEID表。}')
async def _(msg: MessageSession):
    query = msg.parsed_msg['<query>']
    query_options = {'q': query, 'limit': '6'}
    query_url = f'{api}?{urllib.parse.urlencode(query_options)}'
    resp = await get_url(query_url, 200, fmt='json')
    if result := resp['data']['result']:
        plain_texts = [
            f'{x["enumName"]}：{x["key"]} -> {x["value"]}' for x in result[:5]
        ]

        if resp['data']['count'] > 5:
            plain_texts.extend(
                (
                    '...仅显示前5条结果，查看更多：',
                    'https://ca.projectxero.top/idlist/'
                    + resp['data']['hash'],
                )
            )

        await msg.finish('\n'.join(plain_texts))
    else:
        await msg.finish('没有找到结果。')

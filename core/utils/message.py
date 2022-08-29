import re
from typing import Union

from discord import Embed as DiscordEmbed

from core.elements.message.internal import Embed, EmbedField


def removeIneffectiveText(prefix: str, lst: list) -> list:
    '''删除命令首尾的空格和换行以及重复命令。
    
    :param prefix: 机器人的命令前缀。
    :param lst: 字符串（List/Union）。
    :returns: 净化后的字符串。'''
    remove_list = ['\n', ' ']  # 首尾需要移除的东西
    for x in remove_list:
        list_cache = []
        for y in lst:
            split_list = y.split(x)
            for _ in split_list:
                if split_list[0] == '':
                    del split_list[0]
                if len(split_list) > 0 and split_list[-1] == '':
                    del split_list[-1]
            for _ in split_list:
                if len(split_list) > 0:
                    spl0 = split_list[0]
                    if spl0.startswith(prefix) and spl0 != '':
                        split_list[0] = re.sub(f'^{prefix}', '', split_list[0])
            list_cache.append(x.join(split_list))
        lst = list_cache
    duplicated_list = []  # 移除重复命令
    for x in lst:
        if x not in duplicated_list:
            duplicated_list.append(x)
    lst = duplicated_list
    return lst


def removeDuplicateSpace(text: str) -> str:
    '''删除命令中间多余的空格。

    :param text: 字符串。
    :returns: 净化后的字符串。'''
    strip_display_space = text.split(' ')
    display_list = [x for x in strip_display_space if x != '']
    return ' '.join(display_list)


def convertDiscordEmbed(embed: Union[DiscordEmbed, dict]) -> Embed:
    '''将DiscordEmbed转换为Embed。
    :param embed: DiscordEmbed。
    :returns: Embed。'''
    embed_ = Embed()
    if isinstance(embed, DiscordEmbed):
        embed = embed.to_dict()
    if isinstance(embed, dict):
        if 'title' in embed:
            embed_.title = embed['title']
        if 'description' in embed:
            embed_.description = embed['description']
        if 'url' in embed:
            embed_.url = embed['url']
        if 'color' in embed:
            embed_.color = embed['color']
        if 'timestamp' in embed:
            embed_.timestamp = embed['timestamp']
        if 'footer' in embed:
            embed_.footer = embed['footer']['text']
        if 'image' in embed:
            embed_.image = embed['image']
        if 'thumbnail' in embed:
            embed_.thumbnail = embed['thumbnail']
        if 'author' in embed:
            embed_.author = embed['author']
        if 'fields' in embed:
            fields = [
                EmbedField(
                    field_value['name'],
                    field_value['value'],
                    field_value['inline'],
                )
                for field_value in embed['fields']
            ]

            embed_.fields = fields
    return embed_


def split_multi_arguments(lst: list):
    new_lst = []
    for x in lst:
        spl = list(filter(None, re.split(r"(\(.*?\))", x)))
        if len(spl) > 1:
            for y in spl:
                index_y = spl.index(y)
                if mat := re.match(r"\((.*?)\)", y):
                    spl1 = mat[1].split('|')
                    for s in spl1:
                        cspl = spl.copy()
                        cspl.insert(index_y, s)
                        del cspl[index_y + 1]
                        new_lst.append(''.join(cspl))
        elif mat := re.match(r"\((.*?)\)", spl[0]):
            spl1 = mat[1].split('|')
            new_lst.extend(iter(spl1))
        else:
            new_lst.append(spl[0])
    split_more = False
    for n in new_lst:
        if re.match(r"\((.*?)\)", n):
            split_more = True
    return split_multi_arguments(new_lst) if split_more else list(set(new_lst))


__all__ = ['removeDuplicateSpace', 'removeIneffectiveText', 'convertDiscordEmbed', "split_multi_arguments"]

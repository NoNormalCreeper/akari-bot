from .cache import random_cache_path
from core.logger import Logger
from tenacity import retry, wait_fixed, stop_after_attempt
import filetype as ft
from aiofile import async_open
import aiohttp
from typing import Union
import traceback
import socket
import re
import urllib.parse


def private_ip_check(hostname: str) -> bool:
    '''检查是否为私有IP。

    :param hostname: 需要检查的主机名。
    returns: 是否为私有IP。'''
    addr_info = socket.getaddrinfo(hostname, 80)
    private_ips = re.compile(
        r'^(?:127\.|0?10\.|172\.0?1[6-9]\.|172\.0?2[0-9]\.172\.0?3[01]\.|192\.168\.|169\.254\.|::1|[fF][cCdD][0-9a-fA-F]{2}:|[fF][eE][89aAbB][0-9a-fA-F]:)')
    addr = addr_info[0][4][0]
    return True if private_ips.match(addr) else False


@retry(stop=stop_after_attempt(3), wait=wait_fixed(3), reraise=True)
async def get_url(url: str, status_code: int = False, headers: dict = None, fmt=None, log=False, timeout=20):
    """利用AioHttp获取指定url的内容。

    :param url: 需要获取的url。
    :param status_code: 指定请求到的状态码，若不符则抛出ValueError。
    :param headers: 请求时使用的http头。
    :param fmt: 指定返回的格式。
    :param log: 是否输出日志。
    :param timeout: 超时时间。
    :returns: 指定url的内容（字符串）。
    """
    hostname = urllib.parse.urlparse(url).hostname
    check = private_ip_check(hostname)
    if check:
        raise ValueError(
            f'Attempt of requesting private IP addresses is not allowed, requesting {hostname}.')

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout), headers=headers) as req:
            if log:
                Logger.info(await req.read())
            if status_code and req.status != status_code:
                raise ValueError(
                    f'{str(req.status)}[Ke:Image,path=https://http.cat/{str(req.status)}.jpg]')
            if fmt is not None:
                if hasattr(req, fmt):
                    return await getattr(req, fmt)()
                else:
                    raise ValueError(f"NoSuchMethod: {fmt}")
            else:
                text = await req.text()
                return text


@ retry(stop=stop_after_attempt(3), wait=wait_fixed(3), reraise=True)
async def post_url(url: str, data: any, headers: dict = None):
    '''发送POST请求。
    :param url: 需要发送的url。
    :param data: 需要发送的数据。
    :param headers: 请求时使用的http头。
    :returns: 发送请求后的响应。'''
    hostname = urllib.parse.urlparse(url).hostname
    check = private_ip_check(hostname)
    if check:
        raise ValueError(
            'Attempt of requesting private IP addresses is not allowed.')

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data, headers=headers) as req:
            return await req.text()


@ retry(stop=stop_after_attempt(3), wait=wait_fixed(3), reraise=True)
async def download_to_cache(url: str) -> Union[str, bool]:
    '''利用AioHttp下载指定url的内容，并保存到缓存（./cache目录）。

    :param url: 需要获取的url。
    :returns: 文件的相对路径，若获取失败则返回False。'''
    hostname = urllib.parse.urlparse(url).hostname
    check = private_ip_check(hostname)
    if check:
        raise ValueError(
            'Attempt of requesting private IP addresses is not allowed.')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                res = await resp.read()
                ftt = ft.match(res).extension
                path = f'{random_cache_path()}.{ftt}'
                async with async_open(path, 'wb+') as file:
                    await file.write(res)
                    return path
    except:
        Logger.error(traceback.format_exc())
        return False


__all__ = ['get_url', 'post_url', 'download_to_cache']

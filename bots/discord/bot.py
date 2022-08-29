import importlib
import os
import re
import traceback

import discord

from bots.discord.client import client
from bots.discord.message import MessageSession, FetchTarget
from config import Config
from core.elements import MsgInfo, Session, PrivateAssets, Url, Command
from core.logger import Logger
from core.parser.message import parser
from core.utils import init, init_async, load_prompt, MessageTaskManager

PrivateAssets.set(os.path.abspath(f'{os.path.dirname(__file__)}/assets'))
init()
Url.disable_mm = True

count = 0


@client.event
async def on_ready():
    Logger.info(f'Logged on as {str(client.user)}')
    global count
    if count == 0:
        await init_async(FetchTarget)
        await load_prompt(FetchTarget)
        count = 1


slash_load_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'slash'))


def load_slashcommands():
    fun_file = None
    dir_list = os.listdir(slash_load_dir)
    for file_name in dir_list:
        try:
            file_path = os.path.join(slash_load_dir, file_name)
            fun_file = None
            if os.path.isdir(file_path):
                if file_name[0] != '_':
                    fun_file = file_name
            elif os.path.isfile(file_path):
                if file_name[0] != '_' and file_name.endswith('.py'):
                    fun_file = file_name[:-3]
            if fun_file is not None:
                Logger.info(f'Loading slash.{fun_file}...')
                modules = f'bots.discord.slash.{fun_file}'
                importlib.import_module(modules)
                Logger.info(f'Succeeded loaded bots.discord.slash.{fun_file}!')
        except:
            tb = traceback.format_exc()
            errmsg = f'Failed to load bots.discord.slash.{fun_file}: \n{tb}'
            Logger.error(errmsg)


load_slashcommands()


@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return
    target = "Discord|Channel"
    if isinstance(message.channel, discord.DMChannel):
        target = "Discord|DM|Channel"
    targetId = f"{target}|{message.channel.id}"
    replyId = None if message.reference is None else message.reference.message_id
    prefix = None
    if match_at := re.match(r'^<@(.*?)>', message.content):
        if match_at[1] == str(client.user.id):
            prefix = ['']
            message.content = re.sub(r'<@(.*?)>', '', message.content)

    msg = MessageSession(target=MsgInfo(targetId=targetId,
                                        senderId=f"Discord|Client|{message.author.id}",
                                        senderName=message.author.name, targetFrom=target, senderFrom="Discord|Client",
                                        clientName='Discord',
                                        messageId=message.id,
                                        replyId=replyId),
                         session=Session(message=message, target=message.channel, sender=message.author))
    await parser(msg, prefix=prefix)


if dc_token := Config('dc_token'):
    client.run(dc_token)

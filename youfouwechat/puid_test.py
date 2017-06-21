#!/usr/bin/env python3
# coding: utf-8

""" 
这个脚本会自动获取所有用户，包括群聊中的非好友群成员，然后排重，再获取 puid，最后把本次新增和没用到的 puid 和对应用户名称标出来。
可在每次增减结果中检查是否有重复的用户，如果有，则表示该用户的 puid 标记不准确。
"""

import logging

from wxpy import *

logging.basicConfig(level=logging.INFO)

bot = Bot('bot.pkl')

logging.info('enabling puid')
bot.enable_puid()

old_puid_set = set(bot.puid_map.user_names.values())
new_puid_set = set()

logging.info('updating chats into set')
unique_chats = set()
unique_chats.update(bot.chats())

for group in bot.groups():
    logging.info('updating members of {} into set'.format(group))
    # group.update_group(members_details=True)
    unique_chats.update(group.members)

logging.info('getting puid')
for chat in unique_chats:
    puid = chat.puid
    if puid:
        new_puid_set.add(puid)
    else:
        print(chat.raw)

logging.info('unused puid left')
for puid in old_puid_set - new_puid_set:
    print('-', puid, bot.puid_map.captions.get_key(puid))

logging.info('new puid list')
for puid in new_puid_set - old_puid_set:
    print('+', puid, bot.puid_map.captions.get_key(puid))

logging.info('total puids: {}'.format(len(bot.puid_map)))

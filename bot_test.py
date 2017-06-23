#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
from config import *
import re
from wxpy.utils import start_new_thread
import time
import os
from kick_votes import KickVotes
from timed_list import TimedList
from dbm_util import *
'''
使用 cache 来缓存登陆信息，同时使用控制台登陆
'''
bot = Bot('bot.pkl', console_qr=False)
bot.messages.max_history = 0



# 定位公司群
test2 = ensure_one(bot.groups().search('test2'))
yiquntulv = ensure_one(bot.groups().search('test2'))
# 定位老板
tao = ensure_one(test2.search('涛'))
#tao.send('Hello WeChat!')
xiaoi = XiaoI('tAhK6zpeONOs', 'MNdtLQ7ic90kU33WUlsn')
print(sys.path[0]+'\\Hongten.pag')
db = dbm.open(sys.path[0]+'\\puid_key_value.pag', 'c')

'''
开启 PUID 用于后续的控制
'''
bot.enable_puid('wxpy_puid.pkl')


'''
邀请信息处理
'''
rp_new_member_name = (
    re.compile(r'^"(.+)"通过'),
    re.compile(r'邀请"(.+)"加入'),
)

# 格式化 Group
groups = list(map(lambda x: bot.groups().search(puid=x)[0], group_puids))
# 格式化 Admin
admins = list(map(lambda x: bot.friends().search(puid=x)[0], admin_puids))

# 远程踢人命令: 移出 @<需要被移出的人>
rp_kick = re.compile(r'^(?:移出|移除|踢出|拉黑)\s*@(.+?)(?:\u2005?\s*$)')
kick_votes = KickVotes(300)
votes_to_kick = 5
black_list = TimedList()

# 下方为函数定义

def get_time():
    return str(time.strftime("%Y-%m-%d %H:%M:%S"))

'''
机器人消息提醒设置
'''
group_receiver = ensure_one(bot.groups().search(alert_group))
logger = get_wechat_logger(group_receiver)
logger.error(str("机器人登陆成功！"+ get_time()))

'''
重启机器人
'''
def _restart():
    os.execv(sys.executable, [sys.executable] + sys.argv)


'''
定时报告进程状态
'''
def heartbeat():
    while bot.alive:
        time.sleep(3600)
        # noinspection PyBroadException
        try:
            logger.error(get_time() + " 机器人目前在线,共有好友 【" + str(len(bot.friends())) + "】 群 【 " + str(len(bot.groups())) + "】" )
        except ResponseError as e:
            if 1100 <= e.err_code <= 1102:
                logger.critical('LCBot offline: {}'.format(e))
                _restart()

start_new_thread(heartbeat)

'''
条件邀请
'''
def condition_invite(user):
    if user.sex == 2:
        female_groups = bot.groups().search(female_group)[0]
        try:
            female_groups.add_members(user, use_invitation=True)
            pass
        except:
            pass
    if (user.province in city_group.keys() or user.city in city_group.keys()):
        try:
            target_city_group = bot.groups().search(city_group[user.province])[0]
            pass
        except:
            target_city_group = bot.groups().search(city_group[user.city])[0]
            pass
        try:
            if user not in target_city_group:
                target_city_group.add_members(user, use_invitation=True)
        except:
            pass

'''
判断消息发送者是否在管理员列表
'''
def from_admin(msg):
    """
    判断 msg 中的发送用户是否为管理员
    :param msg:
    :return:
    """
    if not isinstance(msg, Message):
        raise TypeError('expected Message, got {}'.format(type(msg)))
    from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
    return from_user in admins

'''
远程踢人命令

def remote_kick(msg):
    if msg.type is TEXT:
        match = rp_kick.search(msg.text)
        if match:
            name_to_kick = match.group(1)

            if not from_admin(msg):
                return '感觉有点不对劲… @{}'.format(msg.member.name)

            member_to_kick = ensure_one(list(filter(
                lambda x: x.name == name_to_kick, msg.chat)))
            if member_to_kick  == bot.self:
                return '无法移出 @{}'.format(member_to_kick.name)
            if member_to_kick in admins:
                return '无法移出 @{}'.format(member_to_kick.name)

            logger.error(get_time() + str(" 【"+member_to_kick.name + "】 被 【"+msg.member.name+"】 移出 【" + msg.sender.name+"】"))
            member_to_kick.set_remark_name("[黑名单]-"+get_time())
            member_to_kick.remove()
            for ready_to_kick_group in  groups:
                if member_to_kick in ready_to_kick_group:
                    ready_to_kick_group.remove_members(member_to_kick)
                    logger.error(get_time()+ str("【"+member_to_kick.name + "】 被系统自动移出 " +  ready_to_kick_group.name))

            return '成功移出 @{}'.format(member_to_kick.name)
'''

@dont_raise_response_error
def try_send(chat, msg):
    """尝试发送消息给指定聊天对象"""

    if chat.is_friend:
        chat.send(msg)

def _kick(to_kick, limit_secs=0, msg=None):
    if limit_secs:
        # 加入计时黑名单
        black_list.set(to_kick, limit_secs)

    to_kick.remove()
    ret = '@{} 已被成功移出! 😈'.format(to_kick.name)

    start_new_thread(try_send, kwargs=dict(chat=to_kick, msg=msg))

    if to_kick in kick_votes:
        voters = kick_votes[to_kick][0]
        voters = '\n'.join(map(lambda x: '@{}'.format(x.name), voters))
        ret += '\n\n投票人:\n{}'.format(voters)

    return ret


def remote_kick(msg):
    info_msg = '抱歉，你已被{}移出，接下来的 24 小时内，机器人将对你保持沉默 😷'
    limit_secs = 3600 * 24
    if msg.type is TEXT:
        print('remote_kick'+msg.text)
        match = rp_kick.search(msg.text)
        if match:
            name_to_kick = match.group(1)

            # Todo: 有重名时的多个选择

            try:
                member_to_kick = ensure_one(msg.chat.search(name=name_to_kick))
            except ValueError:
                member_to_kick = ensure_one(msg.chat.search(nick_name=name_to_kick))

            if member_to_kick in admins:
                logger.error('{} tried to kick {} whom was an admin'.format(
                    msg.member.name, member_to_kick.name))
                return '无法移出管理员 @{} 😷️'.format(member_to_kick.name)

            if from_admin(msg):
                # 管理员: 直接踢出
                return _kick(member_to_kick, limit_secs, info_msg.format('管理员'))
            else:
                # 其他群成员: 投票踢出
                votes, secs_left = kick_votes.vote(voter=msg.member, to_kick=member_to_kick)

                now = time.time()
                voted = 0
                for voters, start in kick_votes.votes.values():
                    if msg.member in voters and now - start < 600:
                        # 10 分钟内尝试投票移出 3 个群员，则认为是恶意用户
                        voted += 1
                        if voted >= 3:
                            _kick(
                                msg.member, limit_secs,
                                '抱歉，你因恶意投票而被移出。接下来的 24 小时内，机器人将对你保持沉默 [悠闲]'
                            )
                            return '移出了恶意投票者 @{} [闪电]'.format(msg.member.name)

                if votes < votes_to_kick:
                    return '正在投票移出 @{}' \
                           '\n当前 {} / {} 票 ({:.0f} 秒有效)' \
                           '\n移出将拉黑 24 小时 😵' \
                           '\n请谨慎投票 🤔'.format(name_to_kick, votes, votes_to_kick, secs_left)
                else:
                    return _kick(member_to_kick, limit_secs, info_msg.format('投票'))


'''
邀请消息处理
'''
def get_new_member_name(msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')

    for rp in rp_new_member_name:
        match = rp.search(msg.text)
        if match:
            return match.group(1)

'''
定义邀请用户的方法。
按关键字搜索相应的群，如果存在相应的群，就向用户发起邀请。
'''
def invite(user, keyword):
    from random import randrange
    group = bot.groups().search(keyword_of_group[keyword])
    if len(group) > 0:
        for i in range(0, len(group)):
            if user in group[i]:
                content = "您已经加入了 {} [微笑]".format(group[i].nick_name)
                user.send(content)
                return
        if len(group) == 1:
            target_group = group[0]
        else:
            index = randrange(len(group))
            target_group = group[index]
        try:
            target_group.add_members(user, use_invitation=True)
        except:
            user.send("邀请错误！机器人邀请好友进群已达当日限制。请您明日再试")
    else:
        user.send("该群状态有误，您换个关键词试试？")

# 下方为消息处理

'''
处理加好友请求信息。
如果验证信息文本是字典的键值之一，则尝试拉群。
'''
@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    if msg.text.lower() in keyword_of_group.keys():
        invite(user, msg.text.lower())
    else:
        user.send(invite_text)

global    msg_myfriend
xiaobingmp = ensure_one(bot.mps().search('图灵机器人'))
@bot.register(Friend)
def exist_friends(msg):
    global    msg_myfriend
    if msg.sender.name.find("黑名单") != -1:
        return "您已被拉黑！"
    else:
        if msg.text.lower() in keyword_of_group.keys():
            invite(msg.sender, msg.text.lower())
        else:
            msg_myfriend=msg
            msg.forward(xiaobingmp)
            pass
#            return invite_text
@bot.register(Group)
def reply_groups(msg):
    global    msg_myfriend
    if '开启聊天' in msg.text.lower():
        db[msg.chat.puid]='True'
        return  '开启聊天'
    if '开启装逼' in msg.text.lower():
        db[msg.chat.puid]='True'
        return  '开启装逼'
    if '关闭聊天' in msg.text.lower():
        db[msg.chat.puid]='False'
        return  '关闭聊天'
    if msg.sender.name.find("黑名单") != -1:
        return "您已被拉黑！"
    else:
        if db[msg.chat.puid] == 'True':
            msg_myfriend=msg
            msg.forward(xiaobingmp)
            pass
#            return invite_text
# 管理群内的消息处理
@bot.register(groups, except_self=False)
def wxpy_group(msg):
    ret_msg = remote_kick_member(msg)
    print('222222222222222'+msg.text)
    global    msg_myfriend
    if ret_msg:
        return ret_msg
    elif  msg.is_at:
        global sms_sent
        if '开启聊天' in msg.text.lower():
            db[msg.chat.puid]='True'
            return  '开启聊天'
        if '开启装逼' in msg.text.lower():
            db[msg.chat.puid]='True'
            return  '开启装逼'
        if '关闭聊天' in msg.text.lower():
            db[msg.chat.puid]='False'
            return  '关闭聊天'
        if turing_key :
            tuling = Tuling(api_key=turing_key)
            tuling.do_reply(msg)
        else:
            msg_myfriend=msg
            msg.forward(xiaobingmp)
#            return "忙着呢，别烦我！";
            pass
    elif msg.type is TEXT:
#        print('msg.chat.puid'+msg.chat.puid)
        if db[msg.chat.puid] == 'True':
            msg_myfriend=msg
            msg.forward(xiaobingmp)
            pass
    elif msg.type is PICTURE:
        if db[msg.chat.puid] == 'True':
            msg_myfriend=msg
            msg.forward(xiaobingmp)
            pass

@bot.register(MP)
def auto_replymp(msg):
#    name = get_new_member_name(msg)
#    print('222222222222222'+msg.text)
    global msg_myfriend
    if msg.type is TEXT:
#        print('msg.text==='+msg.text)
        msg.forward(msg_myfriend.chat)
    elif msg.type is PICTURE:
        msg.forward(msg_myfriend.chat)
 #      time.sleep(15)
 #       xiaoi.do_reply(msg)
 #       msg_myfriend=msg



@bot.register(groups, NOTE)
def welcome(msg):
    name = get_new_member_name(msg)
    if name:
        return welcome_text.format(name)




embed()

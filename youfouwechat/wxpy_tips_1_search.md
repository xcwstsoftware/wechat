# wxpy 小技巧 (1) -- 搜索

wxpy 除了用于自动回复外，在搜索方面也很拿手。

> 是指在自己的好友或已加入的群聊中进行搜索

这里举个针对群的例子~

----


0) 先找到群，并更新群成员详细信息。

```python
from wxpy import *

bot = Bot()
# 找到群
group = ensure_one(bot.groups().search('要找的群名称'))
# 更新群成员详细信息
group.update_group(True)
```

1) 找出所有女群员~

```python
female_members = group.members.search(sex=FEMALE)
```

2) 只想看本地的？那就加个 city 参数吧。

```python
local_female_members = group.members.search(sex=FEMALE, city='深圳')
```

3) 想一次性把她们都加为好友？

```python
local_female_members.add_all(interval=3, verify_content='认识一下吧？')
```

注意设置 `add_all()` 的 `interval` 参数，过高的请求频率可能导致加好友功能被短暂封锁。

----

除了群成员外，bot.friends() 也有 `search()` 方法，可用于在好友中进行搜索。

关于 `search` 的具体说明，请参见 [文档说明](http://wxpy.readthedocs.io/zh/latest/api/chat.html#wxpy.Chats.search)。

更多小技巧，敬请期待。

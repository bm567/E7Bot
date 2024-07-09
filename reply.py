# -*- coding: utf-8 -*-
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message, C2CMessage

from plugin.dogs import dog
from plugin.news import get_news

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        if "舔狗日记" in message.content:
            if dog().status_code == 200:
                send = await self.api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=dog().text)
            else:
                send = await self.api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="接口异常")
        elif "新闻" in message.content:
            n = get_news()
            if n:
                media = await message._api.post_group_file(
                    group_openid=message.group_openid,
                    file_type=1,
                    url=n
                )
                send = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=7,
                    media=media,
                    msg_id=message.id
                )
                _log.info(send)
            else:
                send = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="接口异常")
                _log.info(send)
        # else:
        #     send = await self.api.post_group_message(
        #         group_openid=message.group_openid,
        #         msg_type=0,
        #         msg_id=message.id,
        #         content=f"收到了消息：{message.content}")
        # _log.info(send)

    # async def on_c2c_message_create(self, message: C2CMessage):
    #     if message.attachments:
    #         for attachment in message.attachments:
    #             print(attachment)
    #             if attachment.url:
    #                 image_url = attachment.url
    #                 _log.info(f"Image URL: {image_url}")
    #                 a = await self.api.post_c2c_file(
    #                     openid=message.author.user_openid,
    #                     file_type=1,
    #                     url=image_url,
    #                 )
    #                 await self.api.post_c2c_message(
    #                     openid=message.author.user_openid,
    #                     msg_type=7,
    #                     msg_id=message.id,
    #                     content=f"我收到了你的消息：{message.content}",
    #                     media=a
    #                 )
    #     else:
    #         if message.content == "舔狗日记":
    #             if dog().status_code != 200:
    #                 await self.api.post_c2c_message(
    #                     openid=message.author.user_openid,
    #                     msg_type=0, msg_id=message.id,
    #                     content=f"接口异常"
    #                 )
    #             else:
    #                 await self.api.post_c2c_message(
    #                     openid=message.author.user_openid,
    #                     msg_type=0, msg_id=message.id,
    #                     content=dog().text)
            # else:
            #     await self.api.post_c2c_message(
            #         openid=message.author.user_openid,
            #         msg_type=0, msg_id=message.id,
            #         content=f"我收到了你的消息：{message.content}"
            #     )


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])

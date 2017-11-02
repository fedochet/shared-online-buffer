# -*- coding: utf-8 -*-
import json
import logging
from channels.channel import Group
from channels.message import Message

logger = logging.getLogger(__name__)

READERS_GROUP = 'reader'
EDITORS_GROUP = 'editor'


def ws_connect(message: Message):
    logger.info("{} connected by websocket!".format(message.reply_channel))
    message.reply_channel.send({"accept": True})
    Group('chat').add(message.reply_channel)


def ws_message(message: Message):
    logger.info("Recieved message {} from {}".format(message.content, message.reply_channel))
    if is_first_message(message):
        group = get_message_group(message)
        if group.name == READERS_GROUP:
            group.add(message.reply_channel)

    else:
        Group(READERS_GROUP).send({
            'text': json.dumps({
                'message': message.content['text'],
                'sender': message.reply_channel.name
            })
        })


def ws_disconnect(message: Message):
    logger.info("Websocket {} disconnected!".format(message.reply_channel))
    Group(READERS_GROUP).discard(message.reply_channel)


def is_first_message(message: Message) -> bool:
    text_object = json.loads(message.content['text'])
    return 'role' in text_object


def get_message_group(message: Message) -> Group:
    text_object = json.loads(message.content['text'])
    if 'role' in text_object:
        sender_role = text_object['role']
        return Group(sender_role)

    return Group(READERS_GROUP)


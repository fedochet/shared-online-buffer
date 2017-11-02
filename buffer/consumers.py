# -*- coding: utf-8 -*-
import json
import logging

from channels.channel import Group
from channels.message import Message

from buffer.editors_storage import get_buffer_editor, add_buffer_editor, \
    remove_buffer_editors
from buffer.views import lookup_private, lookup_public

logger = logging.getLogger(__name__)

READERS_GROUP = 'reader'
EDITORS_GROUP = 'editor'

TEXT_ID = 1


def ws_connect(message: Message):
    logger.info("{} connected by websocket!".format(message.reply_channel))
    accept_websocket(message)
    # message.reply_channel.send(text_with_message(get_text(TEXT_ID).text))


def is_reader(message) -> bool:
    text_object = json.loads(message.content['text'])
    return text_object['role'] == 'reader'


def get_buffer_token(message) -> str:
    text_object = json.loads(message.content['text'])
    return text_object['buffer_id']


def ws_message(message: Message):
    logger.info("Recieved message {} from {}".format(message.content, message.reply_channel))
    token = get_buffer_token(message)
    if is_reader(message):
        text_object = lookup_public(token)
        get_readers_group(text_object.id).add(message.reply_channel)
        message.reply_channel.send(text_with_message(text_object.text))
    else:
        text_object = lookup_private(token)
        if get_buffer_editor(text_object.id) is None:
            add_buffer_editor(text_object.id, str(message.reply_channel))
            send_text_to(message.reply_channel, text_object.text)
        elif not registered_editor(message, text_object):
            close_websocket(message)
        else:
            updated_text = json.loads(message.content['text'])['message']
            text_object.text = updated_text
            text_object.save()
            send_text_to_readers(text_object.id, updated_text)


def ws_disconnect(message: Message):
    logger.info("Websocket {} disconnected!".format(message.reply_channel))
    remove_editor_if_matches(message)
    Group(READERS_GROUP).discard(message.reply_channel)


def registered_editor(message, text_object):
    return get_buffer_editor(text_object.id) == str(message.reply_channel)


def accept_websocket(message):
    message.reply_channel.send({"accept": True})


def close_websocket(message):
    message.reply_channel.send({"close": True})


def send_text_to_readers(text_id: int, updated_text: str):
    send_text_to(get_readers_group(text_id), updated_text)


def send_text_to(reciever, text: str):
    reciever.send(text_with_message(text))


def get_readers_group(text_id: int) -> Group:
    return Group("readers_{}".format(text_id))


def remove_editor_if_matches(message):
    if get_buffer_editor(TEXT_ID) == str(message.reply_channel):
        remove_buffer_editors(TEXT_ID)


def is_first_message(message: Message) -> bool:
    text_object = json.loads(message.content['text'])
    return 'first_role' in text_object


def get_message_group(message: Message) -> Group:
    text_object = json.loads(message.content['text'])
    if 'role' in text_object:
        sender_role = text_object['role']
        return Group(sender_role)

    return Group(READERS_GROUP)


def text_with_message(message):
    return {
        'text': json.dumps({
            'message': message,
        })
    }

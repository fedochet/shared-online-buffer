# -*- coding: utf-8 -*-
import json
import logging

from channels.channel import Group
from channels.message import Message

from buffer.editors_storage import get_buffer_editor, add_buffer_editor, \
    remove_buffer_editors
from buffer.views import get as get_text, lookup_private

logger = logging.getLogger(__name__)

READERS_GROUP = 'reader'
EDITORS_GROUP = 'editor'

TEXT_ID = 1


def ws_connect(message: Message):
    logger.info("{} connected by websocket!".format(message.reply_channel))
    accept_websocket(message)
    message.reply_channel.send(text_with_message(get_text(TEXT_ID).text))


def ws_message(message: Message):
    logger.info("Recieved message {} from {}".format(message.content, message.reply_channel))
    if is_first_message(message):
        group = get_message_group(message)
        if group.name == READERS_GROUP:
            group.add(message.reply_channel)
        else:
            if get_buffer_editor(TEXT_ID) is None:
                add_buffer_editor(TEXT_ID, str(message.reply_channel))
                message.reply_channel.send(text_with_message(get_text(TEXT_ID).text))
            else:
                close_websocket(message)
    else:
        updated_text = json.loads(message.content['text'])['message']
        private_token = json.loads(message.content['text'])['buffer_id']
        text_to_change = lookup_private(private_token)
        text_to_change.text = updated_text
        text_to_change.save()
        Group(READERS_GROUP).send(text_with_message(updated_text))


def ws_disconnect(message: Message):
    logger.info("Websocket {} disconnected!".format(message.reply_channel))
    remove_editor_if_matches(message)
    Group(READERS_GROUP).discard(message.reply_channel)


def accept_websocket(message):
    message.reply_channel.send({"accept": True})


def close_websocket(message):
    message.reply_channel.send({"close": True})


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

import json
import logging
from channels.channel import Group
from channels.message import Message

logger = logging.getLogger(__name__)


def ws_connect(message: Message):
    logger.info("{} connected by websocket!".format(message.reply_channel))
    message.reply_channel.send({"accept": True})
    Group('chat').add(message.reply_channel)


def ws_message(message: Message):
    logger.info("Recieved message {} from {}".format(message.content, message.reply_channel))
    Group('chat').send({
        'text': json.dumps({
            'message': message.content['text'],
            'sender': message.reply_channel.name
        })
    })


def ws_disconnect(message: Message):
    logger.info("Websocket {} disconnected!".format(message.reply_channel))
    Group('chat').discard(message.reply_channel)

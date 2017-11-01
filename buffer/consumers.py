import json
from channels.channel import Group
from channels.message import Message


def ws_connect(message: Message):
    print("Connected")
    message.reply_channel.send({"accept": True})
    Group('chat').add(message.reply_channel)


def ws_message(message: Message):
    print("Send message")
    Group('chat').send({
        'text': json.dumps({
            'message': message.content['text'],
            'sender': message.reply_channel.name
        })
    })


def ws_disconnect(message: Message):
    print("Disconnected")
    Group('chat').discard(message.reply_channel)

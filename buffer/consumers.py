import json
from channels.channel import Group


def ws_connect(message):
    print("Connected")
    message.reply_channel.send({"accept": True})
    Group('chat').add(message.reply_channel)


def ws_message(message):
    print("Send message")
    Group('chat').send({'text': json.dumps({'message': message.content['text'],
                                            'sender': message.reply_channel.name})})


def ws_disconnect(message):
    print("Disconnected")
    Group('chat').discard(message.reply_channel)
# Channels
from channels.layers import get_channel_layer


async def send_message(channel_name, message, message_type):
    """
    Update message in web socket
    """
    group_name = channel_name
    channel_layer = get_channel_layer()

    content = {
        # This "type" passes through to the front-end to facilitate
        # our Redux events.
        "type": message_type,
        "payload": message,
    }
    try:
        await channel_layer.group_send(group_name, {
            # This "type" defines which handler on the Consumer gets
            # called.
            "type": "notify",
            "content": content,
        })
    except Exception as e:
        print("WS ERROR 500:", e)

# def send_message(channel_name, message, message_type):
#    async_to_sync(send_message)(channel_name, message, message_type)

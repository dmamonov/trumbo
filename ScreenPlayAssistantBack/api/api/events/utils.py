# Channels
from channels.layers import get_channel_layer


async def update_chat(channel_name, obj_dict, chat_model):
    """
    Update message in web socket
    """
    group_name = channel_name
    channel_layer = get_channel_layer()

    content = {
        # This "type" passes through to the front-end to facilitate
        # our Redux events.
        "type": chat_model,
        "payload": obj_dict,
    }

    await channel_layer.group_send(group_name, {
        # This "type" defines which handler on the Consumer gets
        # called.
        "type": "notify",
        "content": content,
    })

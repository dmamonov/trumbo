# Channels
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# Serializers
from api.ws.serializers import WSSerializer


class WSConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # We're always going to accept the connection, though we may
        # close it later based on other factors.
        await self.accept()

    async def notify(self, event):
        """
        This handles calls elsewhere in this codebase that look
        like:

            channel_layer.group_send(group_name, {
                'type': 'notify',  # This routes it to this handler.
                'content': json_message,
            })

        Don't try to directly use send_json or anything; this
        decoupling will help you as things grow.
        """
        await self.send_json(event["content"])

    async def receive_json(self, content, **kwargs):
        """
        This handles data sent over the wire from the client.

        We need to validate that the received data is of the correct
        form. You can do this with a simple DRF serializer.

        We then need to use that validated data to confirm that the
        requesting user (available in self.scope["user"] because of
        the use of channels.auth.AuthMiddlewareStack in routing) is
        allowed to subscribe to the requested object.
        """

        serializer = WSSerializer(data=content)

        try:
            await sync_to_async(serializer.is_valid)(raise_exception=True)
        except Exception as e:
            print("WEBSOCKET ERROR:", e)
            await self.close(code=4000)
        else:
            # Define this method on your serializer:
            group_names = await sync_to_async(serializer.get_group_names)()

            # The AsyncJsonWebsocketConsumer parent class has a
            # self.groups list already. It uses it in cleanup.
            for group_name in group_names:
                self.groups.append(group_name)
                # This actually subscribes the requesting socket to the
                # named group:
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name,
                )

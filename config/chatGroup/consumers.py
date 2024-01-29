from .utils.extended_consumer import ExtendedAsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import ConsumerMessageCreationSerializer



class ChatGroupConsumer(ExtendedAsyncWebsocketConsumer):
	serializer_class = ConsumerMessageCreationSerializer

	async def connect(self):
		chat_group_pk = self.scope['url_route']['kwargs']['chat_group_pk']
		if self.scope['user'].is_authenticated == False:
			await self.close()
		else:
			self.group_name = 'chatGroup_' + str(chat_group_pk)
			self.channel_layer.group_add(
				self.group_name,
				self.channel_layer
				)
			await self.accept()


	async def disconnect(self, close_code):
		self.channel_layer.group_discard(
				self.group_name,
				self.channel_layer
			)


	async def receive(self, text_data=None, bytes_data=None):
		data = text_data + bytes_data
		serializer = self.get_serializer(data=data)
		validation_result = serializer.is_valid()
		if validation_result == True:
			self.save_model_serializer_data(serializer)


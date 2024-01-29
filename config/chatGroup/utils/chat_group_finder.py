from chatGroup.models import ChatGroup
from .custom_exceptions import NoExistingChatGroup



class ChatGroupFinder:
    def find_chat_group_by_pk(self, chat_group_pk):
        try:
            return ChatGroup.objects.get(pk=chat_group_pk)
        except ChatGroup.DoesNotExist:
            raise NoExistingChatGroup

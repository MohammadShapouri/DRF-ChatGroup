from chatGroup.models import ChatGroupMember
from django.db.models import Q


class AdminOwnerFinder:
    is_user_owner = False
    is_user_admin = False
    chat_group_member_owner_object = None
    chat_group_member_admin_objects = list()
    chat_group_member_admin_pk_list = list()


    def find_owner_and_admins(self, user, chat_group):
        # Unauthenticated users are neither admin not owner and they don't need 'chat_group_member_owner_object',
        # 'chat_group_member_admin_objects' and 'chat_group_member_admin_pk_list'.
        if user.is_authenticated:
            self.chat_group_member_admin_pk_list = list()

            chat_group_member_admin_owner_objects = ChatGroupMember.objects.filter(Q(chat_group=chat_group) & (Q(access_level='admin') | Q(access_level='owner'))).select_related('user')
            for each_object in chat_group_member_admin_owner_objects:
                if each_object.access_level == 'owner':
                    self.chat_group_member_owner_object = each_object
                    if user == self.chat_group_member_owner_object.user:
                        self.is_user_owner = True
                elif each_object.access_level == 'admin':
                    self.chat_group_member_admin_objects.append(each_object)
                    self.chat_group_member_admin_pk_list.append(str(each_object.pk))
                    if user == each_object.user:
                        self.is_user_admin = True





class MembershipStatusDefiner:
    is_member = False


    def define_member_status(self, user, chat_group):
        chat_group_member_objects = ChatGroupMember.objects.filter(Q(chat_group=chat_group)).select_related('user')
        for each_object in chat_group_member_objects:
            if each_object.user == user:
                self.is_member = True
                return self.is_member

        self.is_member = False
        return self.is_member

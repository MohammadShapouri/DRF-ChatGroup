from .pk_cache import ChatGroupPKCahce
from django.db.models import Q
import redis


class AdminOwnerNormalMemberFinder(ChatGroupPKCahce):
    redis_db = redis.Redis(decode_responses=True, host='localhost', port=6379, db=0)
    is_user_owner = False
    is_user_admin = False
    # chat_group_member_owner_object = None
    # chat_group_member_admin_objects = list()
    # chat_group_admins_pk_list = list()
    chat_group_owner_pk = None
    chat_group_admins_pk_list = list()
    chat_group_normal_members_pk_list = list()

    def find_owner_and_admins(self, user, chat_group):
        # Unauthenticated users are neither admin not owner and they don't need 'chat_group_member_owner_object',
        # 'chat_group_member_admin_objects' and 'chat_group_admins_pk_list'.
        if user.is_authenticated:
            self.chat_group_normal_members_pk_list = list()
            self.chat_group_admins_pk_list = list()

            # chat_group_member_admin_owner_objects = ChatGroupMember.objects.filter(Q(chat_group=chat_group) & (Q(access_level='admin') | Q(access_level='owner'))).select_related('user')
            # for each_object in chat_group_member_admin_owner_objects:
            #     if each_object.access_level == 'owner':
            #         self.chat_group_member_owner_object = each_object
            #         if user == self.chat_group_member_owner_object.user:
            #             self.is_user_owner = True
            #     elif each_object.access_level == 'admin':
            #         self.chat_group_member_admin_objects.append(each_object)
            #         self.chat_group_admins_pk_list.append(str(each_object.pk))
            #         if user == each_object.user:
            #             self.is_user_admin = True
            cached_chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group)
            self.chat_group_normal_members_pk_list = list(map(int, cached_chat_group_members_pk_dict.get('normal_users_pk')))
            self.chat_group_admins_pk_list = list(map(int, cached_chat_group_members_pk_dict.get('admins_pk')))
            self.chat_group_owner_pk = int(cached_chat_group_members_pk_dict.get('owner_pk'))
            if int(user.pk) == int(self.chat_group_owner_pk):
                self.is_user_owner = True
            if int(user.pk) in self.chat_group_admins_pk_list:
                self.is_user_admin = True





class MembershipStatusDefiner(ChatGroupPKCahce):
    is_member = False
    chat_group_member_pk_list = list()


    def define_member_status(self, user, chat_group):
        self.chat_group_member_pk_list = list()
        # chat_group_member_objects = ChatGroupMember.objects.filter(Q(chat_group=chat_group)).select_related('user')
        # for each_object in chat_group_member_objects:
        #     if each_object.user == user:
        #         self.is_member = True
        #         return self.is_member
        cached_chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group)
        self.chat_group_member_pk_list = list(map(int, cached_chat_group_members_pk_dict.get('normal_users_pk')))

        if int(user.pk) in self.chat_group_member_pk_list:
            self.is_member = True
            return self.is_member

        self.is_member = False
        return self.is_member

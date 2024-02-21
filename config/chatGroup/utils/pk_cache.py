import redis
import json
from chatGroup.models import ChatGroup, ChatGroupMember


class BasePKCache:
    redis_db = redis.Redis(decode_responses=True, host='localhost', port=6379, db=0)

    def serialize_dict(self, pk_dict):
        if pk_dict == None:
            return None
        else:
            return json.dumps(pk_dict)


    def deserialize_dict(self, pk_dict):
        if pk_dict == None:
            return None
        else:
            return json.loads(pk_dict)
    

    def clean_set_name(self, set_name):
        return (str(set_name)).encode('utf-8').strip()


    def get_cached_set(self, set_name):
        set_name = (str(set_name)).encode('utf-8').strip()
        redis_dict = self.redis_db.get(set_name)
        return self.deserialize_dict(redis_dict)


    def set_cached_set(self, set_name, set_dict):
        set_name = (str(set_name)).encode('utf-8').strip()
        redis_dict = self.serialize_dict(set_dict)
        self.redis_db.set(set_name, redis_dict)


    def remove_cached_set(self, set_name):
        self.redis_db.delete(self.clean_set_name(set_name))





class ChatGroupPKCahce(BasePKCache):


    def initial_caching_at_startup(self):
        checked_chat_groups = list()
        queryset = ChatGroupMember.objects.all().select_related('user').select_related('chat_group').order_by('chat_group__pk')
        for chat_group_member in queryset:
            if chat_group_member.chat_group.pk not in checked_chat_groups:
                checked_chat_groups.append(chat_group_member.chat_group.pk)
                chat_members_data = {
                                    'owner_pk': None,
                                    'admins_pk': [],
                                    'normal_users_pk': []
                                }
                self.set_cached_set_based_on_chat_group_obj(chat_group_member.chat_group, chat_members_data)
                self.add_new_member_to_cached_data(chat_group_member.chat_group, chat_group_member)
            else:
                self.add_new_member_to_cached_data(chat_group_member.chat_group, chat_group_member)





    def cache_new_chat_group(self, chat_group_obj, chat_group_member_obj):
        chat_members_data = {
                            'owner_pk': chat_group_member_obj.user.pk,
                            'admins_pk': [],
                            'normal_users_pk': []
                        }
        self.set_cached_set_based_on_chat_group_obj(chat_group_obj, chat_members_data)

    
    def get_cached_set_based_on_chat_group_obj(self, chat_group_obj):
        return self.get_cached_set(chat_group_obj.pk)


    def set_cached_set_based_on_chat_group_obj(self, chat_group_obj, set_dict):
        self.set_cached_set(chat_group_obj.pk, set_dict)



    def remove_chat_group_cache_based_on_chat_group_obj(self, chat_group_obj):
        self.remove_cached_set(chat_group_obj.pk)


    # It will be called when owner is changed.
    def change_chat_group_ownership_cached_data(self, chat_group_obj, new_chat_group_member_owner_obj, new_chat_group_member_admin_obj):
        chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group_obj)

        # New owner was previously admin.
        new_chat_group_member_owner_user_obj = new_chat_group_member_owner_obj.user
        chat_group_members_pk_dict.get('admins_pk').remove(new_chat_group_member_owner_user_obj.pk)
        chat_group_members_pk_dict['owner_pk'] = new_chat_group_member_owner_user_obj.pk
        # New admin was previously owner.
        chat_group_members_pk_dict.get('admins_pk').append(new_chat_group_member_admin_obj.user.pk)
        self.set_cached_set_based_on_chat_group_obj(chat_group_obj, chat_group_members_pk_dict)


    def change_chat_group_admin_to_normal_member_cached_data(self, chat_group_obj, new_chat_group_member_normal_user_obj):
        chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group_obj)

        # New normal user was previously admin.
        chat_group_members_pk_dict.get('admins_pk').remove(new_chat_group_member_normal_user_obj.user.pk)
        # New normal user was previously admin.
        chat_group_members_pk_dict.get('normal_users_pk').append(new_chat_group_member_normal_user_obj.user.pk)
        self.set_cached_set_based_on_chat_group_obj(chat_group_obj, chat_group_members_pk_dict)


    def change_chat_group_normal_user_to_admin_cached_data(self, chat_group_obj, new_chat_group_member_admin_obj):
        chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group_obj)
        new_chat_group_member_admin_user_obj = new_chat_group_member_admin_obj.user
        # New normal user was previously admin.
        chat_group_members_pk_dict.get('normal_users_pk').remove(new_chat_group_member_admin_user_obj.pk)
        # New normal user was previously admin.
        chat_group_members_pk_dict.get('admins_pk').append(new_chat_group_member_admin_user_obj.pk)
        self.set_cached_set_based_on_chat_group_obj(chat_group_obj, chat_group_members_pk_dict)


    def add_new_member_to_cached_data(self, chat_group_obj, new_chat_group_member_member_obj):
        chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group_obj)
        if new_chat_group_member_member_obj.access_level == 'normal_user':
            chat_group_members_pk_dict.get('normal_users_pk').append(new_chat_group_member_member_obj.user.pk)
        elif new_chat_group_member_member_obj.access_level == 'admin':
            chat_group_members_pk_dict.get('admins_pk').append(new_chat_group_member_member_obj.user.pk)
        elif new_chat_group_member_member_obj.access_level == 'owner':
            chat_group_members_pk_dict['owner_pk'] = new_chat_group_member_member_obj.user.pk
        self.set_cached_set_based_on_chat_group_obj(chat_group_obj, chat_group_members_pk_dict)


    def remove_member_form_chat_group_set(self,chat_group_obj, chat_group_member_member_obj):
        chat_group_members_pk_dict = self.get_cached_set_based_on_chat_group_obj(chat_group_obj)
        if chat_group_member_member_obj.access_level == 'normal_user':
            chat_group_members_pk_dict.get('normal_users_pk').remove(chat_group_member_member_obj.user.pk)
        if chat_group_member_member_obj.access_level == 'admin':
            chat_group_members_pk_dict.get('admins_pk').remove(chat_group_member_member_obj.user.pk)
        if chat_group_member_member_obj.access_level == 'owner':
            chat_group_members_pk_dict['owner_pk'] = None
        self.set_cached_set_based_on_chat_group_obj(chat_group_obj, chat_group_members_pk_dict)


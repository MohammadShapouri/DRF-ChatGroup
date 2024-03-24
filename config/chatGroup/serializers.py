from rest_framework import serializers
from .models import ChatGroup, ChatGroupMember, Message
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils.pk_cache import ChatGroupPKCahce
from extentions.regexValidators.random_link_generator import CallableRandomLinkGenerator

UserAccount = get_user_model()



class ChatGroupCreationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.fields['group_random_username'].read_only = True
        self.fields['creation_date'].read_only = True
        self.fields['group_special_username'].allow_null = True
        self.fields['group_special_username'].allow_blank = True
        # UNAUTHENTICATED USERS ACCESS TO THIS SERIALIZER MUST BE RESTRICTED IN VIEWS.
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            self.fields['owner'] = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all(), label='Owner', required=True, allow_null=False)


    class Meta:
        model = ChatGroup
        fields = ['pk', 'group_name', 'bio', 'group_special_username', 'group_random_username', 'is_public', 'is_forward_allowed', 'writing_access', 'media_uploading_access', 'add_users_by_members', 'creation_date']



    def validate(self, attrs):
        if self.request.data.get('is_public') == None or self.request.data.get('is_public') == '':
            attrs['is_public'] = True
        if self.request.data.get('is_forward_allowed') == None or self.request.data.get('is_forward_allowed') == '':
            attrs['is_forward_allowed'] = True
        if self.request.data.get('add_users_by_members') == None or self.request.data.get('add_users_by_members') == '':
            attrs['add_users_by_members'] = True
        if attrs.get('is_public') == True:
            if attrs.get('group_special_username') == None:
                raise serializers.ValidationError({'detail': "Public groups require special username."})
            elif attrs.get('group_special_username') == '' or str(attrs.get('group_special_username')).strip() == '':
                raise serializers.ValidationError({'group_special_username': 'This field may not be blank when you want to create a public group.'})
            if len(ChatGroup.objects.filter(Q(is_public=True) and Q(group_special_username=attrs.get('group_special_username')))) != 0:
                raise serializers.ValidationError({'detail': "username is already in use."})
        return attrs



    def save(self, **kwargs):
        self.validated_data['group_random_username'] = CallableRandomLinkGenerator()
        return super().save(**kwargs)





class ChatGroupUpdateSerializer(serializers.ModelSerializer, ChatGroupPKCahce):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')
        # self.chat_group = self.context.get('chat_group')

        self.is_user_owner = self.context.get('is_user_owner')
        self.is_user_admin = self.context.get('is_user_admin')
        self.chat_group_owner_pk = self.context.get('chat_group_owner_pk')
        self.chat_group_admins_pk_list = self.context.get('chat_group_admins_pk_list')
        self.chat_group_normal_members_pk_list = self.context.get('chat_group_normal_members_pk_list')
        self.fields['creation_date'].read_only = True
        self.fields['group_random_username'].read_only = True
        self.fields['group_name'].required = False
        self.fields['group_name'].allow_null = False
        self.fields['group_name'].allow_blank = False
        self.fields['group_special_username'].allow_null = True
        self.fields['group_special_username'].allow_blank = True
        # UNAUTHENTICATED USERS ACCESS TO THIS SERIALIZER MUST BE RESTRICTED IN VIEWS.
        if (self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff)) or (self.is_user_owner):
            self.fields['owner'] = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.filter(Q(pk=self.chat_group_owner_pk) | Q(pk__in=self.chat_group_admins_pk_list) | Q(pk__in=self.chat_group_normal_members_pk_list)), label='Owner', required=False, allow_null=False)


    class Meta:
        model = ChatGroup
        fields = ['pk', 'group_name', 'bio', 'group_special_username', 'group_random_username', 'is_public', 'is_forward_allowed', 'writing_access', 'media_uploading_access', 'creation_date']


    def validate(self, attrs):
        if attrs.get('is_public') == True:
            if attrs.get('group_special_username') == None:
                raise serializers.ValidationError({'detail': "Public groups require special username."})
            elif attrs.get('group_special_username') == '' or str(attrs.get('group_special_username')).strip() == '':
                raise serializers.ValidationError({'group_special_username': 'This field may not be blank when you want to make a group public.'})
            if len(ChatGroup.objects.filter(Q(is_public=True) and Q(group_special_username=attrs.get('group_special_username')))) != 0:
                raise serializers.ValidationError({'detail': "username is already in use."})

        # According to serializer fields restrictions, the following if block works when
        # superuser or staff or group owner use update method and change owner of group.
        owner = attrs.get('owner')
        if owner != None:
            if int(owner.pk) == int(self.chat_group_owner_pk):
                attrs.pop('owner', None)
            elif int(owner.pk) not in self.chat_group_admins_pk_list:
                raise serializers.ValidationError({'detail': "new owner must be selected from group admins." +
                                                            " To give this user ownership of group, change its access level to admin first."})
        return attrs


    def save(self, **kwargs):
        if self.validated_data.get('is_public') == False:
            self.validated_data['group_special_username'] = None
        return super().save(**kwargs)





class ChatGroupRetrievalSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.is_user_owner = self.context.get('is_user_owner')
        self.is_user_admin = self.context.get('is_user_admin')
        if self.request.user.is_authenticated and ((self.request.user.is_superuser or self.request.user.is_staff) or self.is_user_owner or self.is_user_admin):
            fields = ['pk', 'group_name', 'bio', 'group_special_username', 'group_random_username', 'is_public', 'is_forward_allowed', 'writing_access', 'media_uploading_access', 'creation_date']
        else:
            fields = ['pk', 'group_name', 'bio', 'group_special_username', 'is_public', 'is_forward_allowed', 'writing_access', 'media_uploading_access', 'creation_date']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for fieldname in existing - allowed:
            self.fields.pop(fieldname)


    class Meta:
        model = ChatGroup
        fields = ['pk', 'group_name', 'bio', 'group_special_username', 'group_random_username', 'is_public', 'is_forward_allowed', 'writing_access', 'media_uploading_access', 'creation_date']





class ChatGroupMemberCreationSerializer(serializers.ModelSerializer, ChatGroupPKCahce):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.chat_group = self.context.get('chat_group')
        self.is_user_owner = self.context.get('is_user_owner')
        self.is_user_admin = self.context.get('is_user_admin')
        self.fields['chat_group'].read_only = True
        self.fields['chat_group'].required = False
        self.fields['joined_at'].read_only = True
        self.fields['group_random_username'] = serializers.CharField(required=False, allow_null=True, allow_blank=True, label=ChatGroup._meta.get_field('group_random_username').verbose_name.title())
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
            fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']
        else:
            self.fields['access_level'].read_only = True
            fields = ['pk', 'chat_group', 'user', 'access_level', 'joined_at', 'group_random_username']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for fieldname in existing - allowed:
            if fieldname != 'group_random_username':
                self.fields.pop(fieldname)



    class Meta:
        model = ChatGroupMember
        fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']


    def validate(self, attrs):
        chat_group_member_objects = ChatGroupMember.objects.filter(chat_group=self.chat_group).select_related('user').select_related('chat_group')
        for i in range(len(chat_group_member_objects)):
                if attrs.get('user') == chat_group_member_objects[i].user:
                    raise serializers.ValidationError({'user': "User is already a member of this chat group."})

        if (self.request.user.is_superuser == False or self.request.user.is_staff == False or self.is_user_admin == False or self.is_user_owner == False) and self.chat_group.add_users_by_members == False:
            for i in range(len(chat_group_member_objects)):
                if self.request.user == chat_group_member_objects[i].user:
                    break
                else:
                    if i == len(chat_group_member_objects)-1:
                        raise serializers.ValidationError({'chat_group': "You can't add users to a chat group which you are not a member of that."})

        if self.chat_group.is_public == False and self.request.user.is_superuser == False and self.request.user.is_staff == False and self.is_user_admin == False and self.is_user_owner == False:
            if attrs.get('group_random_username') == None:
                group_random_link_verbose_name = ChatGroup._meta.get_field('group_random_username').verbose_name.title()
                raise serializers.ValidationError({'chat_group': f"{group_random_link_verbose_name} is required for joining private groups."})
            elif attrs.get('group_special_username') == '' or str(attrs.get('group_special_username')).strip() == '':
                raise serializers.ValidationError({'group_special_username': 'This field may not be blank when you want to join a private group.'})
            elif attrs.get('group_special_username') != self.chat_group.group_special_username:
                raise serializers.ValidationError({'group_special_username': 'This username is incorrect.'})   
        return attrs





class ChatGroupMemberUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')
        self.is_user_owner = self.context.get('is_user_owner')
        self.is_user_admin = self.context.get('is_user_admin')
        self.fields['joined_at'].read_only = True
        self.fields['chat_group'].read_only = True
        self.fields['chat_group'].required = False
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff):
            fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']
        else:
            self.fields['user'].read_only = True
            self.fields['joined_at'].read_only = True
            if self.is_user_owner:
                fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']
            elif self.is_user_admin:
                fields = ['pk', 'chat_group', 'user', 'member_nickname', 'joined_at']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for fieldname in existing - allowed:
            self.fields.pop(fieldname)


    class Meta:
        model = ChatGroupMember
        fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']


    def validate(self, attrs):
        if attrs.get('access_level') == 'owner':
            if self.instance.access_level == 'normal_user':
                raise serializers.ValidationError({'access_level': "Normal users can't become owner directly, change its access level to admin first."})
            if self.instance.access_level == 'owner':
                attrs.pop('owner', None)
        return attrs





class ChatGroupMemberRetrievalSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')
        self.is_user_owner = self.context.get('is_user_owner')
        self.is_user_admin = self.context.get('is_user_admin')
        if self.user.is_authenticated and ((self.user.is_superuser or self.user.is_staff) or self.is_user_owner or self.is_user_admin):
            fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']
        else:
            fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for fieldname in existing - allowed:
            self.fields.pop(fieldname)


    class Meta:
        model = ChatGroupMember
        fields = ['pk', 'chat_group', 'user', 'access_level', 'member_nickname', 'joined_at']





class MessageRetrievalSerializer(serializers.ModelSerializer):
    # UNAUTHENTICATED USERS ACCESS TO THIS SERIALIZER MUST BE RESTRICTED IN VIEWS AND CONSUMERS.


    class Meta:
        model = Message
        fields = '__all__'





# class ViewSetMessageCreationSerializer(serializers.ModelSerializer):
#     # UNAUTHENTICATED USERS ACCESS TO THIS SERIALIZER MUST BE RESTRICTED IN VIEWS.
#     def __init__(self, *args, **kwargs):
#         self.user = self.context.get('user')
#         self.chat_group = self.context.get('chat_group')
#         self.fields['message'].required = False
#         self.fields['creation_date'].read_only = True
#         self.fields['updated_at'].read_only = True
#         self.fields['chat_group'].read_only = True
#         self.fields['file1'] = serializers.FileField(required=False, label='File 1')
#         self.fields['file2'] = serializers.FileField(required=False, label='File 2')
#         self.fields['file3'] = serializers.FileField(required=False, label='File 3')
#         self.fields['file4'] = serializers.FileField(required=False, label='File 4')
#         self.fields['file5'] = serializers.FileField(required=False, label='File 5')


#     class Meta:
#         model = Message
#         fields = ['pk', 'writer', 'chat_group', 'message', 'replied_to', 'created_at', 'updated_at']


#     def validate(self, attrs):
#         if self.request.user.is_authenticated and (self.request.user.is_superuser == False or self.request.user.is_staff == False):
#             member_chat_group_objects = ChatGroupMember.objects.filter(user=self.user).select_related('chat_group')
#             for i in range(len(member_chat_group_objects)):
#                     if self.chat_group == member_chat_group_objects[i].chat_group:
#                         break
#                     else:
#                         if i == len(member_chat_group_objects)-1:
#                             raise serializers.ValidationError({'chat_group': "You can't send message to a chat group which you are not a member of that."})
#         if attrs.get("file1", None) == None and\
#         attrs.get("file2", None) == None and\
#         attrs.get("file3", None) == None and\
#         attrs.get("file4", None) == None and\
#         attrs.get("file5", None) == None:
#             if attrs.get('message', None) == None:
#                 raise serializers.ValidationError({'message': "A text message is required when you don't want to send any file."})
#         return attrs


#     def save(self, validated_data):
#         validated_data['writer'] = self.user
#         return super().save(validated_data)





# class ViewSetMessageUpdateSerializer(serializers.ModelSerializer):
#     # UNAUTHENTICATED USERS ACCESS TO THIS SERIALIZER MUST BE RESTRICTED IN VIEWS.
#     def __init__(self, *args, **kwargs):
#         self.user = self.context.get('user')
#         self.fields['message'].required = False
#         self.fields['creation_date'].read_only = True
#         self.fields['updated_at'].read_only = True
#         if self.request.user.is_authenticated and (self.request.user.is_superuser == False or self.request.user.is_staff == False):
#             self.fields['writer'].read_only = True
#             self.fields['replied_to'].read_only = True


#     class Meta:
#         model = Message
#         fields = ['pk', 'writer', 'chat_group', 'message', 'replied_to', 'created_at', 'updated_at']


#     def validate(self, attrs):
#         if self.request.user.is_authenticated and (self.request.user.is_superuser == False or self.request.user.is_staff == False):
#             member_chat_group_objects = ChatGroupMember.objects.filter(user=self.user).select_related('chat_group')
#             for i in range(len(member_chat_group_objects)):
#                     if attrs.get('chat_group') == member_chat_group_objects[i].chat_group:
#                         break
#                     else:
#                         if i == len(member_chat_group_objects)-1:
#                             raise serializers.ValidationError({'chat_group': "You can't send message to a chat group which you are not a member of that."})
#         if attrs.get("file1", None) == None and\
#         attrs.get("file2", None) == None and\
#         attrs.get("file3", None) == None and\
#         attrs.get("file4", None) == None and\
#         attrs.get("file5", None) == None:
#             if attrs.get('message', None) == None:
#                 raise serializers.ValidationError({'message': "A text message is required when you don't want to send any file."})
#         return attrs





class ConsumerMessageCreationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.scope = self.context.get('scope')
        self.fields['message'].required = False
        self.fields['creation_date'].read_only = True
        self.fields['updated_at'].read_only = True
        self.fields.pop('file', None)

    class Meta:
        model = Message
        fields = '__all__'


    def validate(self, attrs):
        if self.scope.user.is_authenticated and (self.scope.user.is_superuser == False or self.scope.user.is_staff == False):
            member_chat_group_objects = ChatGroupMember.objects.filter(user=self.user).select_related('chat_group')
            for i in range(len(member_chat_group_objects)):
                    if attrs.get('chat_group') == member_chat_group_objects[i].chat_group:
                        break
                    else:
                        if i == len(member_chat_group_objects)-1:
                            raise serializers.ValidationError({'chat_group': "You can't send message to a chat group which you are not a member of that."})
        if attrs.get("file1", None) == None and\
        attrs.get("file2", None) == None and\
        attrs.get("file3", None) == None and\
        attrs.get("file4", None) == None and\
        attrs.get("file5", None) == None:
            if attrs.get('message', None) == None:
                raise serializers.ValidationError({'message': "A text message is required when you don't want to send any file."})
        return attrs


    # def create(self, validated_data):

    #     return instance




class ConsumerMessageUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.scope = self.context.get('scope')
        self.fields['message'].required = False
        self.fields['creation_date'].read_only = True
        self.fields['updated_at'].read_only = True
        self.fields.pop('file', None)

    class Meta:
        model = Message
        fields = '__all__'


    def validate(self, attrs):
        if self.scope.user.is_authenticated and (self.scope.user.is_superuser == False or self.scope.user.is_staff == False):
            member_chat_group_objects = ChatGroupMember.objects.filter(user=self.user).select_related('chat_group')
            for i in range(len(member_chat_group_objects)):
                    if attrs.get('chat_group') == member_chat_group_objects[i].chat_group:
                        break
                    else:
                        if i == len(member_chat_group_objects)-1:
                            raise serializers.ValidationError({'chat_group': "You can't send message to a chat group which you are not a member of that."})
        if attrs.get("file1", None) == None and\
        attrs.get("file2", None) == None and\
        attrs.get("file3", None) == None and\
        attrs.get("file4", None) == None and\
        attrs.get("file5", None) == None:
            if attrs.get('message', None) == None:
                raise serializers.ValidationError({'message': "A text message is required when you don't want to send any file."})
        return attrs

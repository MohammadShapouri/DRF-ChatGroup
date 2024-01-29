from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ChatGroup, ChatGroupMember, Message, MessageFile
from django.db.models import Q
from .utils.chat_group_users_finder import AdminOwnerFinder, MembershipStatusDefiner
from .utils.chat_group_finder import ChatGroupFinder
from .serializers import (
                        ChatGroupCreationSerializer,
                        ChatGroupRetrivalSerializer,
                        ChatGroupUpdateSerializer,
                        ChatGroupMemberCreationSerializer,
                        ChatGroupMemberRetrivalSerializer,
                        ChatGroupMemberUpdateSerializer,
                        )
from .utils.custom_exceptions import (
                        NoExistingChatGroup,
                        NoExistingChatGroupMember,
                        NoExistingMessage,
                        NormalMembersAccessRestriction,
                        NormalMembersAndAdminsAccessRestriction,
                        NormalMembersDeletingAccessRestriction,
                        AdminsAndNormalMembersAccessRestriction,
                        OnlyMembersAccess,
                        )
# Create your views here.



class ChatGroupViewSet(ModelViewSet, AdminOwnerFinder):
    queryset = ChatGroup.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = None
        try:
            obj = queryset.get(**filter_kwargs)
        except ChatGroup.DoesNotExist:
            raise NoExistingChatGroup

        self.check_object_permissions(self.request, obj)
        self.find_owner_and_admins(self.request.user, obj)
        return obj



    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatGroupRetrivalSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return ChatGroupUpdateSerializer
        elif self.request.method == 'POST':
            return ChatGroupCreationSerializer
        elif self.request.method == 'DELETE':
            return None
        return super().get_serializer_class()



    def get_permissions(self):
        if self.request.method == 'POST' or\
        self.request.method == 'PUT' or\
        self.request.method == 'PATCH' or\
        self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
                        'request': self.request,
                        'is_user_owner': self.is_user_owner,
                        'is_user_admin': self.is_user_admin,
                        'chat_group_member_owner_object': self.chat_group_member_owner_object,
                        'chat_group_member_admin_pk_list': self.chat_group_member_admin_pk_list
                        })
        return context



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner = None
        if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
            owner = serializer.validated_data.pop('owner', None)
            serializer.fields.pop('owner', None)
        else:
            owner = request.user

        obj = serializer.save()
        ownerObj = ChatGroupMember.objects.create(
                                    chat_group = obj,
                                    user = owner,
                                    access_level = "owner"
                                    )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.request.user.is_authenticated == False or\
        (self.request.user.is_superuser == False and self.request.user.is_staff == False)\
        and self.is_user_owner == False and self.is_user_admin == False:
            raise NormalMembersAccessRestriction

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        new_owner = serializer.validated_data.pop('owner', None)
        serializer.fields.pop('owner', None)
        if new_owner != None:
            for each_chat_group_member_admin_object in self.chat_group_member_admin_objects:
                if each_chat_group_member_admin_object == new_owner:
                    each_chat_group_member_admin_object.access_level = "owner"
                    each_chat_group_member_admin_object.save()
                    self.chat_group_member_owner_object.access_level = "admin"
                    self.chat_group_member_owner_object.save()
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)



    def destroy(self, request, *args, **kwargs):
        if self.user.is_authenticated == False or\
        ((self.user.is_superuser == False and self.user.is_staff == False)\
        and self.is_user_owner == False):
            raise NormalMembersAndAdminsAccessRestriction

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)





class ChatGroupMemberViewSet(ModelViewSet, AdminOwnerFinder, ChatGroupFinder, MembershipStatusDefiner):
    permission_classes = [IsAuthenticated]
    chat_group = None

    def get_queryset(self):
        chat_group_pk = self.kwargs.get('chat_group_pk')
        self.chat_group = self.find_chat_group_by_pk(chat_group_pk)

        if self.user.is_authenticated and self.user.is_superuser or self.user.is_staff:
            queryset = ChatGroupMember.objects.get(chat_group=self.chat_group)
            return queryset
        else:
            self.define_member_status(self.request.user, self.chat_group)
            if self.is_member:
                queryset = ChatGroupMember.objects.get(chat_group=self.chat_group)
                return queryset
        raise OnlyMembersAccess



    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except ChatGroupMember.DoesNotExist:
            raise NoExistingChatGroupMember

        self.check_object_permissions(self.request, obj)
        self.find_owner_and_admins(self.request.user, self.chat_group)
        return obj



    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatGroupMemberRetrivalSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return ChatGroupMemberUpdateSerializer
        elif self.request.method == 'POST':
            return ChatGroupMemberCreationSerializer
        elif self.request.method == 'DELETE':
            return None
        return super().get_serializer_class()



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
                        'request': self.request,
                        'is_user_owner': self.is_user_owner,
                        'is_user_admin': self.is_user_admin,
                        'chat_group': self.chat_group
                        })



    def create(self, request, *args, **kwargs):
        chat_group_pk = self.kwargs.get('chat_group_pk')
        self.chat_group = self.find_chat_group_by_pk(chat_group_pk)
        self.find_owner_and_admins(request.user, self.chat_group)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chat_group=self.chat_group)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.request.user.is_authenticated == False or\
        (self.request.user.is_superuser == False and self.request.user.is_staff == False)\
        and self.is_user_owner == False and self.is_user_admin == False:
            raise NormalMembersAccessRestriction

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        accessLevel = serializer.validated_data.get('access_level')
        serializer.save()
        if accessLevel == 'owner':
            self.chat_group_member_owner_object.access_level = "admin"
            self.chat_group_member_owner_object.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.access_level == 'owner' or instance.access_level == 'admin':
            if self.user.is_authenticated == False and\
            (self.user.is_superuser == False and self.user.is_staff == False)\
            and self.is_user_owner == False:
                raise AdminsAndNormalMembersAccessRestriction

        if instance.user != request.user:
            if self.user.is_authenticated == False and\
            (self.user.is_superuser == False and self.user.is_staff == False)\
            and self.is_user_admin == False and self.is_user_owner == False:
                raise NormalMembersDeletingAccessRestriction

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)






class MessageViewSet(ModelViewSet, AdminOwnerFinder, ChatGroupFinder, MembershipStatusDefiner):
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        chat_group_pk = self.kwargs.get('chat_group_pk')
        self.chat_group = self.find_chat_group_by_pk(chat_group_pk)

        if self.user.is_authenticated and self.user.is_superuser or self.user.is_staff:
            queryset = Message.objects.get(chat_group=self.chat_group)
            return queryset
        else:
            self.define_member_status(self.request.user, self.chat_group)
            if self.is_member:
                queryset = Message.objects.get(chat_group=self.chat_group)
                return queryset
        raise OnlyMembersAccess


    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except Message.DoesNotExist:
            raise NoExistingMessage

        self.check_object_permissions(self.request, obj)
        self.find_owner_and_admins(self.request.user, self.chat_group)
        return obj


    def create(self, request, *args, **kwargs):
        chat_group_pk = self.kwargs.get('chat_group_pk')
        self.chat_group = self.find_chat_group_by_pk(chat_group_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        fileList = list()
        # fileList.append(serializer.validated_data.pop('file1', None))
        # serializer.fields.pop('file1', None)

        # fileList.append(serializer.validated_data.pop('file2', None))
        # serializer.fields.pop('file2', None)

        # fileList.append(serializer.validated_data.pop('file3', None))
        # serializer.fields.pop('file3', None)

        # fileList.append(serializer.validated_data.pop('file4', None))
        # serializer.fields.pop('file4', None)

        # fileList.append(serializer.validated_data.pop('file5', None))
        # serializer.fields.pop('file5', None)

        # serializer.save(chat_group=self.chat_group)

        # fileList.remove(None)
        # MessageFile.objects.bulk_create(
        #     MessageFile
        #     )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

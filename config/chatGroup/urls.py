from django.urls import path
from . import views
from rest_framework import routers
from .utils.pk_cache import ChatGroupPKCahce



# This method will be ran once after runserver to cache PKs.
chat_group_pk_cahce = ChatGroupPKCahce()
chat_group_pk_cahce.initial_caching_at_startup()



router = routers.SimpleRouter()
router.register('chatgroups', views.ChatGroupViewSet, basename='ChatGroup')
router.register('members/<chat_group_pk>', views.MessageViewSet, basename='Member')





chatGroupMemberViewSet_list = views.ChatGroupMemberViewSet.as_view({
	'get': 'list',
	'post': 'create'
	})
chatGroupMemberViewSet_detail = views.ChatGroupMemberViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
	})

chatGroupMemberViewSet_urlpatterns = [
	path('chatgroups/<int:chat_group_pk>/chatgroupmembers', chatGroupMemberViewSet_list, name='ChatGroupMember-list'),
	path('chatgroups/<int:chat_group_pk>/chatgroupmembers/<int:pk>', chatGroupMemberViewSet_detail, name='ChatGroupMember-detail')
]





messageViewSet_list = views.MessageViewSet.as_view({
	'get': 'list',
	'post': 'create'
	})
messageViewSet_detail = views.MessageViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
	})

messageViewSet_urlpatterns = [
	path('chatgroups/<int:chat_group_pk>/messages', messageViewSet_list, name='Message-list'),
	path('chatgroups/<int:chat_group_pk>/messages/<int:pk>', messageViewSet_detail, name='Message-detail')
]





urlpatterns = [
]
urlpatterns += router.urls
urlpatterns += chatGroupMemberViewSet_urlpatterns
urlpatterns += messageViewSet_urlpatterns


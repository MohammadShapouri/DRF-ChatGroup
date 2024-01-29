from django.contrib import admin
from .models import ChatGroup, ChatGroupMember
# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(ChatGroupMember)

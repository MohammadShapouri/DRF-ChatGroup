from rest_framework.exceptions import APIException
from rest_framework import status



class NoExistingChatGroup(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"detail": "No chat group found."}
    default_code = 'no chat group'


class NoExistingChatGroupMember(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"detail": "No chat group member found."}
    default_code = 'no chat group member'


class NoExistingMessage(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"detail": "No message found."}
    default_code = 'no message'


class NormalMembersAccessRestriction(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "Normal members of chat group can't access this method."}
    default_code = 'normal members access denied'


class NormalMembersAndAdminsAccessRestriction(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "Normal members and admins of chat group can't access this method."}
    default_code = 'normal members and admins access denied'


class OnlyMembersAccess(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "Only members of this group have access to this data."}
    default_code = 'restricted to memberships'


class AdminsAndNormalMembersAccessRestriction(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "Admins and normal members of chat group can't access this method."}
    default_code = 'admins and normal members access denied'



class NormalMembersDeletingAccessRestriction(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "Normal members of chat group can't remove other users."}
    default_code = 'normal users access denied'


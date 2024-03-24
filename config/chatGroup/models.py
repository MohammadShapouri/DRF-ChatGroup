import os
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
from extentions.regexValidators.ASCII_username_validator import ASCIIUsernameValidator
from extentions.regexValidators.random_link_generator import CallableRandomLinkGenerator
# Create your models here.



class ChatGroup(models.Model):
    WRITING_ACCESS = (
        ('only_owner', 'Only owner'),
        ('only_owner_and_admins', 'only owner and admins'),
        ('all', 'All types of users'),
    )
    MEDIA_UPLOADING_ACCESS = (
        ('only_owner', 'Only owner'),
        ('only_owner_and_admins', 'only owner and admins'),
        ('all', 'All types of users'),
    )

    group_name              = models.CharField(max_length=25, verbose_name='Chat Group Name')
    bio                     = models.CharField(blank=True, null=True, max_length=75, verbose_name='Chat Group Bio')
    group_special_username  = models.SlugField(blank=True, null=True, validators=[ASCIIUsernameValidator], verbose_name='Chat Group Special Username Link')
    group_random_username   = models.SlugField(blank=True, null=True, unique=True, verbose_name='Chat Group Random Username Link')
    is_public               = models.BooleanField(default=True, verbose_name='Is Chat Group Public?')
    is_forward_allowed      = models.BooleanField(default=True, verbose_name='Is Forward Allowed?')
    writing_access          = models.CharField(max_length=21, choices=WRITING_ACCESS, verbose_name='Writing Access Level')
    media_uploading_access  = models.CharField(max_length=21, choices=MEDIA_UPLOADING_ACCESS, verbose_name='Media Uploading Access Level')
    add_users_by_members    = models.BooleanField(default=True, verbose_name='Can other users add new members?')
    creation_date           = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    # >>> If allow_forward is disabled, then ManyToMany() field in Message table will be
    # treated as ForeignKey().

    class Meta:
        verbose_name = "Chat Group"
        verbose_name_plural = "Chat Groups"

    def __str__(self):
        return str(self.group_name) + ' -- ' + str(self.group_random_username)


    def save(self, *args, **kwargs):
        if not self.id:
            self.group_random_username = CallableRandomLinkGenerator()
        if self.writing_access == None:
            self.writing_access = 'all'
        if self.media_uploading_access == None:
            self.media_uploading_access = None
        self.full_clean()
        super().save(*args, **kwargs)



    # Validates Group Special Username. It's useful when we want to create groups in django admin panel.
    def clean(self):
        messages = {
            "requires_value": "%(group_special_username)s is required when you set %(is_public)s to true.",
            "duplicate_value": "%(username)s was used previously."
            }
        codes = {
            "requires_value": "requires_value",
            "duplicate_value": "duplicate_value"
            }
        if self.is_public ==True:
            if self.group_special_username == None or self.group_special_username == '' or self.group_special_username.strip() == '':
                params = {
                            "group_special_username": ChatGroup._meta.get_field('group_special_username').verbose_name.title() ,
                            "is_public": ChatGroup._meta.get_field('group_special_username').verbose_name.title()
                        }
                raise ValidationError(messages['requires_value'], codes['requires_value'], params)

        if self.is_public == False:
            self.group_special_username = None
            return

        if len(ChatGroup.objects.filter(Q(is_public=True) and Q(group_special_username=self.group_special_username))) != 0:
            params = {"username": self.group_special_username}
            raise ValidationError(messages['duplicate_value'], codes['duplicate_value'], params)





class ChatGroupMember(models.Model):
    ACCESS_LEVEL = (
        ('normal_user', 'Normal User'),
        ('admin', 'Admin'),
        ('owner', 'Owner')
    )

    chat_group      = models.ForeignKey('ChatGroup', on_delete=models.CASCADE, verbose_name='Related Chat Group')
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Joined User')
    access_level    = models.CharField(choices=ACCESS_LEVEL, default='normal_user', max_length=11, verbose_name='User Access Level')
    member_nickname = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nickname')
    joined_at       = models.DateTimeField(auto_now_add=True, verbose_name='Joining Date')

    class Meta:
        verbose_name = "Chat Group Member"
        verbose_name_plural = "Chat Group Members"

    def __str__(self):
        return str(self.chat_group) + ' -- ' + str(self.user.pk)
    

    # def save(self, *args, **kwargs):
    #     if self.pk == None and (self.access_level == None or (self.access_level).strip() == ''):
    #         self.access_level = 'normal_user'
    #     return super().save(*args, **kwargs)





class Message(models.Model):
    writer      = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='Writer')
    chat_group  = models.ManyToManyField('ChatGroup', verbose_name='Related Chat Group')
    message     = models.CharField(max_length=500, verbose_name='Message')
    file        = models.ManyToManyField('MessageFile', verbose_name='Message File')
    replied_to  = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, verbose_name='Replied to', related_name='replies')
    created_at  = models.DateTimeField(auto_now=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"





def update_filename(instance, filename):
    splitted_file_name = filename.split('.')
    extention = splitted_file_name[-1]
    filename = '.'.join(splitted_file_name[0:(len(splitted_file_name)-1)])
    filename = filename + '__' + str(timezone.now().timestamp())
    filePath = "uploadedFiles/{0}.{1}".format(filename, extention)
    return os.path.join('group_uploaded_files', filePath)


class MessageFile(models.Model):
    file    = models.FileField(upload_to=update_filename, verbose_name='File')

    class Meta:
        verbose_name = "Message File"
        verbose_name_plural = "Message Files"









# def update_filename(instance, filename):
#     splitted_file_name = filename.split('.')
#     extention = splitted_file_name[-1]
#     filename = '.'.join(splitted_file_name[0:(len(splitted_file_name)-1)])
#     filename = filename + '__' + str(timezone.now().timestamp())
#     filePath = "group_{0}/{1}.{2}".format(instance.chat_group.pk, filename, extention)
#     return os.path.join('profile_photo', filePath)


# class ChatGroupProfilePicture(models.Model):
#     chat_group      = models.ForeignKey('UserAccount', on_delete=models.CASCADE, related_name='photos', verbose_name='User Account Profile Picture')
#     photo           = models.ImageField(upload_to=update_filename, blank=False, null=False, verbose_name='Profile Picture')
#     is_default_pic  = models.BooleanField(default=True, blank=False, null=False, verbose_name='Is It Default Profile Picture?')
#     creation_date   = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='This Profile Picture\'s Creation Date')


#     class Meta:
#         verbose_name = 'User Account Profile Picture'
#         verbose_name_plural = 'User Account Profile Pictures'


#     def __str__(self):
#         return str(self.user) + "'s profile picture -- " + str(self.creation_date)

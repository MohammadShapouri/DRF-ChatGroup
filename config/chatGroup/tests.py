from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .models import ChatGroup, ChatGroupMember
from .utils.pk_cache import ChatGroupPKCahce
# Create your tests here.



class ChatGroupTest(APITestCase, ChatGroupPKCahce):
    maxDiff = None

    def setUp(self):
        # Creating 5 users.
        UserModel = get_user_model()
        superuser = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234000',
            email = 'testuser0@mail.com',
            is_account_verified = True,
            is_active = True,
            is_superuser = True,
            is_staff = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        user_1 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234111',
            email = 'testuser1@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        user_2 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234222',
            email = 'testuser2@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        user_3 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234333',
            email = 'testuser3@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        user_4 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234444',
            email = 'testuser4@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        user_5 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234555',
            email = 'testuser5@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )





    def tearDown(self):
        # Deleting 5 users.
        UserModel = get_user_model()
        UserModel.objects.raw('DELETE FROM userAccount_useraccount')





    def test_initial_caching_at_startup(self):
        self.flush_redis_db()
        UserModel = get_user_model()

        chat_group_1 = ChatGroup.objects.create(
            group_name = "group 1",
            group_random_username = "qwertyuiopasdfghjk1",
            is_public = False,
            is_forward_allowed = True,
            writing_access = "all",
            media_uploading_access = "all"
        )

        chat_group_2 = ChatGroup.objects.create(
            group_name = "group 2",
            group_random_username = "qwertyuiopasdfghjk2",
            is_public = False,
            is_forward_allowed = True,
            writing_access = "all",
            media_uploading_access = "all"
        )

        user_1 = UserModel.objects.get(phone_number="09361234111")
        user_2 = UserModel.objects.get(phone_number="09361234222")
        user_3 = UserModel.objects.get(phone_number="09361234333")
        user_4 = UserModel.objects.get(phone_number="09361234444")
        user_5 = UserModel.objects.get(phone_number="09361234555")

        chat_group_member__1_to_1 = ChatGroupMember.objects.create(
            chat_group = chat_group_1,
            user = user_1,
            access_level = 'owner'
        )

        chat_group_member__2_to_1 = ChatGroupMember.objects.create(
            chat_group = chat_group_1,
            user = user_2,
            access_level = 'admin'
        )

        chat_group_member__3_to_2 = ChatGroupMember.objects.create(
            chat_group = chat_group_2,
            user = user_3,
            access_level = 'admin'
        )

        chat_group_member__4_to_2 = ChatGroupMember.objects.create(
            chat_group = chat_group_2,
            user = user_4,
            access_level = 'admin'
        )

        chat_group_member__5_to_2 = ChatGroupMember.objects.create(
            chat_group = chat_group_2,
            user = user_5,
            access_level = 'normal_user'
        )

        chat_group_pk_cahce = ChatGroupPKCahce()
        chat_group_pk_cahce.initial_caching_at_startup()


        # Validating results.
        self.assertDictEqual(self.get_cached_set_based_on_chat_group_obj(chat_group_1), {'owner_pk': user_1.pk, 'admins_pk': [user_2.pk], 'normal_users_pk': []})
        self.assertDictEqual(self.get_cached_set_based_on_chat_group_obj(chat_group_2), {'owner_pk': None, 'admins_pk': [user_3.pk, user_4.pk], 'normal_users_pk': [user_5.pk]})





    def test_chat_group_creation_1(self):
        # Testing chat group creation by normal user.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "test_special_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "True",
            "add_users_by_members": "False",
            "writing_access": "only_owner_and_admins",
            "media_uploading_access": "only_owner_and_admins",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        chat_group_owner_obj = UserModel.objects.get(phone_number="09361234111")
        self.assertEqual(chat_group_member_obj.user, chat_group_owner_obj)
        self.assertEqual(chat_group_owner_obj.pk, self.get_cached_set_based_on_chat_group_obj(chat_group_member_obj.chat_group).get('owner_pk'))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, "test_special_username")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, True)
        self.assertEqual(chat_group_member_obj.chat_group.add_users_by_members, False)
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, True)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner_and_admins")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner_and_admins")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)





    def test_chat_group_creation_2(self):
        # Testing chat group creation by normal user.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "test_special_username",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "only_owner_and_admins",
            "media_uploading_access": "only_owner_and_admins",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        chat_group_owner_obj = UserModel.objects.get(phone_number="09361234111")
        self.assertEqual(chat_group_member_obj.user, chat_group_owner_obj)
        self.assertEqual(chat_group_owner_obj.pk, self.get_cached_set_based_on_chat_group_obj(chat_group_member_obj.chat_group).get('owner_pk'))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, None)
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, False)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, False)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner_and_admins")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner_and_admins")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)





    def test_chat_group_creation_3(self):
        # Testing chat group creation by normal user.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "test_special_username",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "blah blah",
            "media_uploading_access": "blah blah",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.data['writing_access'][0], "\"blah blah\" is not a valid choice.")        
        self.assertEqual(response.data['media_uploading_access'][0], "\"blah blah\" is not a valid choice.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





    def test_chat_group_creation_4(self):
        # Testing chat group creation by normal user.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.data['group_special_username'][0], "This field may not be blank when you want to create a public group.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





    def test_chat_group_creation_5(self):
        # Testing chat group creation by normal user.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "ff .g",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.data['group_special_username'][0], "Enter a valid username. This value may contain only English letters, "
                                                    "numbers, and @/./+/-/_ characters.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





    def test_chat_group_creation_6(self):
        # Testing chat group creation by superuser.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "false",
            "is_forward_allowed": "False",
            "writing_access": "only_owner_and_admins",
            "media_uploading_access": "only_owner_and_admins",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        # user_4 is chat group owner.
        self.assertEqual(chat_group_member_obj.user, user_4)
        self.assertEqual(user_4.pk, self.get_cached_set_based_on_chat_group_obj(chat_group_member_obj.chat_group).get('owner_pk'))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, None)
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, False)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, False)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner_and_admins")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner_and_admins")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)





    def test_chat_group_update_1(self):
        # Testing chat group update by owner.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Updating chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': response.data['pk']})
        data = {
            "group_name": "test new group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "only_owner",
            "media_uploading_access": "only_owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')

        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        self.assertEqual(chat_group_member_obj.user, UserModel.objects.get(phone_number="09361234111"))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test new group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, None)
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, False)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, False)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)





    def test_chat_group_update_2(self):
        # Testing chat group update by owner.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Updating chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': response.data['pk']})
        data = {
            "group_name": "test new group_name",
            "group_special_username": "group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "True",
            "writing_access": "only_owner",
            "media_uploading_access": "only_owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        self.assertEqual(chat_group_member_obj.user, UserModel.objects.get(phone_number="09361234111"))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test new group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, "group_username")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, True)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, True)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)






    def test_chat_group_update_2(self):
        # Testing chat group update by owner.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Updating chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': response.data['pk']})
        data = {
            "group_name": "test new group_name",
            "group_special_username": "group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "True",
            "writing_access": "only_owner",
            "media_uploading_access": "only_owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        self.assertEqual(chat_group_member_obj.user, UserModel.objects.get(phone_number="09361234111"))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test new group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, "group_username")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, True)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, True)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)





    def test_chat_group_update_3(self):
        # Testing chat group update by owner.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        user_4 = UserModel.objects.get(phone_number='09361234444')
        data = {
            "owner": user_4.pk,
            "group_name": "test group_name",
            "group_special_username": "group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Updating chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': response.data['pk']})
        data = {
            "group_name": "test new group_name",
            "group_special_username": "new_group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "True",
            "writing_access": "only_owner",
            "media_uploading_access": "only_owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        chat_group_member_obj = ChatGroupMember.objects.filter(chat_group=response.data['pk']).select_related('chat_group').select_related('user')[0]
        self.assertEqual(chat_group_member_obj.user, UserModel.objects.get(phone_number="09361234111"))
        self.assertEqual(chat_group_member_obj.chat_group.group_name, "test new group_name")
        self.assertEqual(chat_group_member_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_obj.chat_group.group_special_username, "new_group_username")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_obj.chat_group.is_public, True)
        self.assertEqual(chat_group_member_obj.chat_group.is_forward_allowed, True)
        self.assertEqual(chat_group_member_obj.chat_group.writing_access, "only_owner")
        self.assertEqual(chat_group_member_obj.chat_group.media_uploading_access, "only_owner")
        self.assertNotEqual(chat_group_member_obj.chat_group.creation_date, None)





    def test_chat_group_update_4(self):
        # Testing chat group update by superuser. -- An admin will become owner by superuser.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        user_1 = UserModel.objects.get(phone_number='09361234111')
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_group_pk = response.data['pk']


        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Adding an admin.
        user_3 = UserModel.objects.get(phone_number='09361234333')
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "user": user_3.pk,
            "access_level": "admin",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Updating chat group. -- Changing owner
        url = reverse('ChatGroup-detail', kwargs={'pk': chat_group_pk})
        data = {
            "owner": user_3.pk,
            "group_name": "test new group_name",
            "group_special_username": "group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "True",
            "writing_access": "only_owner",
            "media_uploading_access": "only_owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # getting owner ChatGroupMember object.
        chat_group_member_owner_obj = ChatGroupMember.objects.filter(Q(chat_group=chat_group_pk) & Q(access_level='owner')).select_related('chat_group').select_related('user')[0]
        self.assertEqual(chat_group_member_owner_obj.user, user_3)
        self.assertEqual(chat_group_member_owner_obj.user.pk, self.get_cached_set_based_on_chat_group_obj(chat_group_member_owner_obj.chat_group).get('owner_pk'))
        # getting admin ChatGroupMember object.
        chat_group_member_admin_obj = ChatGroupMember.objects.filter(Q(chat_group=chat_group_pk) & Q(access_level='admin')).select_related('chat_group').select_related('user')[0]
        self.assertEqual(chat_group_member_admin_obj.user, user_1)
        self.assertEqual(chat_group_member_admin_obj.user.pk, self.get_cached_set_based_on_chat_group_obj(chat_group_member_owner_obj.chat_group).get('admins_pk')[0])

        self.assertEqual(chat_group_member_admin_obj.chat_group.group_name, "test new group_name")
        self.assertEqual(chat_group_member_admin_obj.chat_group.bio, None)
        self.assertEqual(chat_group_member_admin_obj.chat_group.group_special_username, "group_username")
        self.assertNotEqual(chat_group_member_admin_obj.chat_group.group_random_username, "ran")
        self.assertNotEqual(chat_group_member_admin_obj.chat_group.group_random_username, None)
        self.assertEqual(chat_group_member_admin_obj.chat_group.is_public, True)
        self.assertEqual(chat_group_member_admin_obj.chat_group.is_forward_allowed, True)
        self.assertEqual(chat_group_member_admin_obj.chat_group.writing_access, "only_owner")
        self.assertEqual(chat_group_member_admin_obj.chat_group.media_uploading_access, "only_owner")
        self.assertNotEqual(chat_group_member_admin_obj.chat_group.creation_date, None)





    def test_chat_group_update_5(self):
        # Testing chat group update by superuser. -- A normal user should't become owner.

        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_group_pk = response.data['pk']



        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Adding a normal user.
        user_3 = UserModel.objects.get(phone_number='09361234333')
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "user": user_3.pk,
            "access_level": "normal_user",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)





        # Updating chat group. -- Chaning owner
        url = reverse('ChatGroup-detail', kwargs={'pk': chat_group_pk})
        data = {
            "owner": user_3.pk,
            "group_name": "test new group_name",
            "group_special_username": "group_username",
            "group_random_username": "ran",
            "is_public": "True",
            "is_forward_allowed": "True",
            "writing_access": "only_owner",
            "media_uploading_access": "only_owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'][0], "new owner must be selected from group admins." +
                                                            " To give this user ownership of group, change its access level to admin first.")





    def test_chat_group_destroy_1(self):
        # Testing deleting chat group by its owner.
        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_group_pk = response.data['pk']


        # Deleting chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': chat_group_pk})
        response = self.client.delete(url, headers=headers, format='json')


        # Validating results. -- cached data was deleted. it was checked in views.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(ChatGroup.objects.filter(pk=chat_group_pk)), 0)





    def test_chat_group_destroy_2(self):
        # Testing deleting chat group by its superuser.
        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_group_pk = response.data['pk']


        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Deleting chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': chat_group_pk})
        response = self.client.delete(url, headers=headers, format='json')


        # Validating results. -- cached data was deleted. it was checked in views.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(ChatGroup.objects.filter(pk=chat_group_pk)), 0)





    def test_chat_group_destroy_3(self):
        # Testing deleting chat group by its admin.
        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_group_pk = response.data['pk']


        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Adding an admin.
        user_3 = UserModel.objects.get(phone_number='09361234333')
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "user": user_3.pk,
            "access_level": "normal_user",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Authenticating admin.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234333",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Deleting chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': chat_group_pk})
        response = self.client.delete(url, headers=headers, format='json')


        # Validating results. -- cached data was deleted. it was checked in views.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Normal members and admins of chat group can't access this method.")





    def test_chat_group_destroy_4(self):
        # Testing deleting chat group by one of its users.
        UserModel = get_user_model()

        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "",
            "group_random_username": "ran",
            "is_public": "False",
            "is_forward_allowed": "False",
            "writing_access": "all",
            "media_uploading_access": "all",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_group_pk = response.data['pk']


        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Adding an admin.
        user_3 = UserModel.objects.get(phone_number='09361234333')
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "user": user_3.pk,
            "access_level": "admin",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Authenticating admin.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234333",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Deleting chat group.
        url = reverse('ChatGroup-detail', kwargs={'pk': chat_group_pk})
        response = self.client.delete(url, headers=headers, format='json')


        # Validating results. -- cached data was deleted. it was checked in views.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Normal members and admins of chat group can't access this method.")












class ChatGroupMemberTest(APITestCase, ChatGroupPKCahce):
    maxDiff = None

    def setUp(self):
        # Creating 5 users.
        UserModel = get_user_model()
        self.superuser = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234000',
            email = 'testuser0@mail.com',
            is_account_verified = True,
            is_active = True,
            is_superuser = True,
            is_staff = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        self.user_1 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234111',
            email = 'testuser1@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        self.user_2 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234222',
            email = 'testuser2@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        self.user_3 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234333',
            email = 'testuser3@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        self.user_4 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234444',
            email = 'testuser4@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        self.user_5 = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234555',
            email = 'testuser5@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )



        # Creating 2 chat groups.
        self.chat_group_1 = ChatGroup.objects.create(
            group_name = "group 1",
            group_random_username = "qwertyuiopasdfghjk1",
            is_public = False,
            is_forward_allowed = True,
            writing_access = "all",
            media_uploading_access = "all"
        )
        self.chat_group_2 = ChatGroup.objects.create(
            group_name = "group 2",
            group_special_username = "special_username_2",
            group_random_username = "qwertyuiopasdfghjk2",
            add_users_by_members = False,
            is_public = True,
            is_forward_allowed = True,
            writing_access = "all",
            media_uploading_access = "all"
        )
        # Creating 2 chat group members.
        self.chat_group_member__1_to_1 = ChatGroupMember.objects.create(
            chat_group = self.chat_group_1,
            user = self.user_1,
            access_level = 'owner'
        )
        self.chat_group_member__2_to_2 = ChatGroupMember.objects.create(
            chat_group = self.chat_group_2,
            user = self.user_2,
            access_level = 'owner'
        )
        # Caching
        chat_group_pk_cahce = ChatGroupPKCahce()
        chat_group_pk_cahce.initial_caching_at_startup()


    def tearDown(self):
        # Deleting 5 users.
        UserModel = get_user_model()
        UserModel.objects.raw('DELETE FROM userAccount_useraccount')
        ChatGroup.objects.raw('DELETE FROM chatGroup_chatgroup')
        ChatGroupMember.objects.raw('DELETE FROM chatGroup_chatgroupmember')
        self.flush_redis_db()



    def test_chat_group_member_creation_1(self):
        # Testing joining private chat group by user itself.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [response.data['user']])
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_creation_2(self):
        # Testing adding member to private chat group by its admin.

        # Adding admin.
        chat_group_member__2_to_1 = ChatGroupMember.objects.create(
            chat_group = self.chat_group_1,
            user = self.user_2,
            access_level = 'admin'
        )

        # Authenticating user 2.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234222",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [response.data['user']])
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_creation_3(self):
        # Testing adding member to private chat group by its owner.

        # Authenticating user 1 -- Group's owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [response.data['user']])
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_creation_4(self):
        # Testing adding member to private chat group without special username by superuser.

        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # adding member to the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "owner")
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), int(response.data['user']))
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_creation_5(self):
        # Testing joining private chat group again.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertNotEqual(response.data['joined_at'], None)


        # Joining the chat group again
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['user'][0], "User is already a member of this chat group.")





    def test_chat_group_member_creation_6(self):
        # Testing adding public chat group by a user who is not a member of group.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_2.pk})
        data = {
            "chat_group": self.chat_group_2.pk,
            "user": self.user_4.pk,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['chat_group'][0], "You can't add users to a chat group which you are not a member of that.")





    def test_chat_group_member_creation_7(self):
        # Testing joining private chat group without special username by a normal user.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_4.pk,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        group_random_link_verbose_name = ChatGroup._meta.get_field('group_random_username').verbose_name.title()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['chat_group'][0], f"{group_random_link_verbose_name} is required for joining private groups.")





    def test_chat_group_member_creation_8(self):
        # Testing joining private chat group without special username by owner.

        # Authenticating owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "test_special_username",
            "is_public": "False",
            "is_forward_allowed": "True",
            "add_users_by_members": "False",
            "writing_access": "only_owner_and_admins",
            "media_uploading_access": "only_owner_and_admins",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_pk = response.data['pk']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # adding member to the chat group by owner
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "chat_group": chat_group_pk,
            "user": self.user_4.pk,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], chat_group_pk)
        self.assertEqual(response.data['user'], self.user_4.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(ChatGroup.objects.get(pk=chat_group_pk)).get('normal_users_pk'), [response.data['user']])
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_creation_9(self):
        # Testing joining private chat group without special username by admin.

        # Authenticating owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating chat group.
        url = reverse('ChatGroup-list')
        data = {
            "group_name": "test group_name",
            "group_special_username": "test_special_username",
            "is_public": "False",
            "is_forward_allowed": "True",
            "add_users_by_members": "False",
            "writing_access": "only_owner_and_admins",
            "media_uploading_access": "only_owner_and_admins",
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_pk = response.data['pk']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # adding member to the chat group by owner
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "chat_group": chat_group_pk,
            "user": self.user_4.pk,
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # changing member access level from normal user to admin.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': chat_group_pk, 'pk': response.data['pk']})
        data = {
            "access_level": "admin"
        }
        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # authenticating new admin
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234444",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # adding member to the chat group by admin
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': chat_group_pk})
        data = {
            "chat_group": chat_group_pk,
            "user": self.user_3.pk
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chat_group'], chat_group_pk)
        self.assertEqual(response.data['user'], self.user_3.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(ChatGroup.objects.get(pk=chat_group_pk)).get('admins_pk'), [self.user_4.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(ChatGroup.objects.get(pk=chat_group_pk)).get('normal_users_pk'), [self.user_3.pk])
        self.assertNotEqual(response.data['joined_at'], None)




    def test_chat_group_member_update_1(self):
        # Testing updating user by owner.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_member_pk = response.data['pk']

        # Authenticating owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # changing member nickname.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "member_nickname": "my lovely user"
        }
        response = self.client.put(url, data=data, headers=headers, format='json')
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [self.user_5.pk])
        self.assertEqual(response.data['member_nickname'], "my lovely user")
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_update_2(self):
        # Testing updating user by owner.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_member_pk = response.data['pk']
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [self.user_5.pk])


        # Authenticating owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # changing member nickname and access level to admin.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "admin",
            "member_nickname": "my lovely user"
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "admin")
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_5.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [])
        self.assertEqual(response.data['member_nickname'], "my lovely user")
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_update_3(self):
        # Testing updating user by owner.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_member_pk = response.data['pk']
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [self.user_5.pk])


        # Authenticating owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # changing member nickname and access level to admin.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "admin",
            "member_nickname": "my lovely user"
        }
        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_5.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [])



        # changing member access level to owner.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "owner",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "owner")
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), self.user_5.pk)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_1.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [])
        self.assertEqual(response.data['member_nickname'], "my lovely user")
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_update_4(self):
        # Testing updating user by owner.

        # Authenticating user 5.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Joining the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "group_random_username": self.chat_group_1.group_random_username,
            "access_level": "owner"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_member_pk = response.data['pk']
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [self.user_5.pk])


        # Authenticating owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234111",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # changing member nickname and access level to admin.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "admin",
            "member_nickname": "my lovely user"
        }
        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_5.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [])



        # changing member access level to owner.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "owner",
            "member_nickname": ""
        }
        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), self.user_5.pk)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_1.pk])
        self.assertEqual(response.data['member_nickname'], "")

        # Authenticating user 5 -- new owner.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234555",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # changing member access level of previous owner to normal user.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': ChatGroupMember.objects.get(Q(user__phone_number="09361234111") & Q(chat_group=self.chat_group_1)).pk})
        data = {
            "access_level": "normal_user",
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_1.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), self.user_5.pk)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [self.user_1.pk])
        self.assertEqual(response.data['member_nickname'], None)
        self.assertNotEqual(response.data['joined_at'], None)





    def test_chat_group_member_update_5(self):
        # Testing updating user by superuser.

        # Authenticating superuser.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09361234000",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        # adding member to the chat group
        url = reverse('ChatGroupMember-list', kwargs={'chat_group_pk': self.chat_group_1.pk})
        data = {
            "chat_group": self.chat_group_1.pk,
            "user": self.user_5.pk,
            "access_level": "normal_user"
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        chat_group_member_pk = response.data['pk']
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "normal_user")
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), self.user_1.pk)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [self.user_5.pk])


        # changing member access level to admin.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "admin",
            "member_nickname": ""
        }
        response = self.client.put(url, data=data, headers=headers, format='json')

        chat_group_member_admin_obj = ChatGroupMember.objects.get(Q(chat_group=self.chat_group_1) & Q(access_level='admin'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "admin")
        self.assertEqual(self.user_5, chat_group_member_admin_obj.user)
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), self.user_1.pk)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_5.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [])
        self.assertEqual(response.data['member_nickname'], "")


        # changing member nickname and access level to owner.
        url = reverse('ChatGroupMember-detail', kwargs={'chat_group_pk': self.chat_group_1.pk, 'pk': chat_group_member_pk})
        data = {
            "access_level": "owner",
            "member_nickname": "my lovely user"
        }
        response = self.client.put(url, data=data, headers=headers, format='json')

        chat_group_member_admin_obj = ChatGroupMember.objects.get(Q(chat_group=self.chat_group_1) & Q(access_level='admin'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat_group'], self.chat_group_1.pk)
        self.assertEqual(response.data['user'], self.user_5.pk)
        self.assertEqual(response.data['access_level'], "owner")
        self.assertEqual(self.user_1, chat_group_member_admin_obj.user)
        self.assertEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('owner_pk'), self.user_5.pk)
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('admins_pk'), [self.user_1.pk])
        self.assertListEqual(self.get_cached_set_based_on_chat_group_obj(self.chat_group_1).get('normal_users_pk'), [])









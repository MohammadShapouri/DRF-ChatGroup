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


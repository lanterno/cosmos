import re
from django.urls import reverse
from django.core import mail
from django.conf import settings

from rest_framework.test import APITestCase

from ..models import User
from .factories import UnactivatedUserFactory, ActivatedUserFactory, ClosedAccountFactory


class UserTests(APITestCase):

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@home.com',
            password='123qwe',
        )
        self.assertEqual(admin.is_superuser, True)
        self.assertEqual(admin.is_staff, True)
        self.assertEqual(admin.check_password('123qwe'), True)

    def test_user_full_and_short_names(self):
        # A user with an email should have full_name return his email.
        email = "someuser@home.com"
        u = User.objects.create_user(email=email, password='123qwe')
        self.assertEqual(u.get_full_name(), email)
        self.assertEqual(u.get_short_name(), '')
        # when a user gets a name, get_full name should return it.
        u.first_name = 'Jack'
        u.save()
        self.assertEqual(u.get_short_name(), 'Jack')  # short name is first_name
        self.assertEqual(u.get_full_name(), u.first_name)
        u.last_name = 'Reacher'
        u.save()
        self.assertEqual(u.get_full_name(), u.first_name + ' ' + u.last_name)
        self.assertEqual(u.get_short_name(), 'Jack')  # short name should still be just first_name

    def test_user_registration_flow_without_mail_validation(self):
        # test system has no users
        self.assertEqual(User.objects.count(), 1)
        # test user signup
        response = self.client.post(
            reverse('auth:user-create'),
            data={
                'email': 'cal@krypton.com',
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 201, response.data)
        # test user exists
        self.assertEqual(User.objects.count(), 2, response.data)

        # test user can't login
        response = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': 'cal@krypton.com',
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 400, response.content)

        # Activate user manually in this test
        user = User.objects.get(email='cal@krypton.com')
        user.is_active = True
        user.save()

        # test user can login after activation
        response = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': 'cal@krypton.com',
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 200, response.content)

    def test_user_can_login_and_see_profile(self):
        user = ActivatedUserFactory.create()
        response = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': user.email,
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 200)
        token = 'Token ' + response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION=token)
        # Now, user should be logged-in
        response = self.client.get(
            reverse('auth:user'),
        )
        self.assertEqual(response.status_code, 200)

    def test_loggedin_user_can_disable_account(self):
        user = ActivatedUserFactory.create()
        self.client.login(email=user.email, password='123qwe')
        # Now, user should be logged-in

        response = self.client.post(
            reverse('auth:disable_account')
        )
        self.assertEqual(response.status_code, 200)
        # call it again to make sure user isn't authenticated anymore
        response = self.client.post(
            reverse('auth:disable_account')
        )
        self.assertEqual(response.status_code, 401)

    def test_user_can_reactivate_account(self):
        user = ClosedAccountFactory()

        # test user can't login
        self.assertFalse(self.client.login(email=user.email, password='123qwe'))

        # call login with activate=True
        response = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': user.email,
                'password': '123qwe',
                'activate': True
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_unverified_users_cant_activate_their_accounts_illegally(self):
        """
        This is to test that unverified users can't login by setting
        activate=True
        """
        user = UnactivatedUserFactory()

        # call login with activate=True
        response = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': user.email,
                'password': '123qwe',
                'activate': True
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_unverified_users_and_wrong_credentials_and_closed_accounts_get_different_error_messages(self):
        unactivated_user = UnactivatedUserFactory()
        closed_account = ClosedAccountFactory()

        response1 = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': unactivated_user.email,
                'password': '123qwe',
            }
        ).json()

        response2 = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': closed_account.email,
                'password': '123qwe',
            }
        ).json()

        self.assertNotEqual(response1, response2)

        response3 = self.client.post(
            reverse('auth:token-create'),
            data={
                'email': 'Wrong_email@home.com',
                'password': '123qwe',
            }
        ).json()

        self.assertNotEqual(response1, response3)
        self.assertNotEqual(response2, response3)

    def test_verify_mail(self):
        self.client.post(
            reverse('auth:user-create'),
            data={
                'email': 'tester@home.com',
                'password': '123qwe'
            }
        )
        user = User.objects.last()

        activation_mail = mail.outbox[0]

        pattern = re.compile(r"\/auth\/activate\/(?P<uid>[\w_-]*)\/(?P<token>[\w_-]*)")

        match = pattern.search(activation_mail.body)

        self.assertEqual(user.email_verified, False)
        self.assertEqual(user.is_active, False)
        response = self.client.post(
            path=reverse('auth:activate'),
            data=match.groupdict()
        )
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.email_verified, True)


class CreateSuperUserSignalTest(APITestCase):

    def test_superuser_is_created_from_settings(self):

        if settings.CREATE_SUPERUSER:
            self.assertEqual(User.objects.count(), 1)
            user = User.objects.first()
            self.assertEqual(user.email, settings.SUPERUSER_EMAIL)
        else:
            self.assertEqual(User.objects.count(), 0)


class IndirectUserCreationTests(APITestCase):

    def test_can_create_user_without_password(self):
        user = User.objects.create_user(email="blabla@somewhere.com", password=None)
        self.assertEqual(user.has_usable_password(), False)

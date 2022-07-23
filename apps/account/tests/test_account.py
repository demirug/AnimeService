import tempfile

from django.conf import settings
from django.templatetags.static import static
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator as generator
from django.utils.crypto import salted_hmac

from apps.account.forms import AccountLoginForm, UserPasswordChangeForm, AccountUpdateForm, UserCreationForm, \
    AccountResetConfirmForm
from apps.account.models import User
from apps.account.views import AccountLogoutView, AccountLoginView, AccountChangePasswordView, AccountProfileView, \
    AccountSubscribersView, AccountRegisterView, ValidateEmailView, AccountEmailChangeView, AccountResetView, \
    AccountResetConfirmView
from apps.movie.models import Anime, Subscribe


class AccountTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username="test", email="test@gmail.com",
                                                  password="test")
        self.client = Client()

    def test_change_lang(self):
        # Test change language midddleware
        self.client.login(username="test", password="test")

        response = self.client.get("/uk/")
        self.user.refresh_from_db(fields=['lang'])
        self.assertEqual(self.user.lang, "uk")

        response = self.client.get("/en/")
        self.user.refresh_from_db(fields=['lang'])
        self.assertEqual(self.user.lang, "en")

    def test_user_avatar(self):
        self.assertEqual(self.user.get_avatar(), static("account/images/default_avatar.png"))

    def test_email(self):
        User.objects.create_user(username="test_2", email="test_2@gmail.com", password="test_2")

    def test_manager(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username="test_3", email=None, password="test_3")

    def test_logout(self):
        response = self.client.get(reverse("account:logout"))
        self.assertEqual(response.resolver_match.func.__name__, AccountLogoutView.as_view().__name__)
        self.assertEqual(response.status_code, 302)

    def test_login_response(self):
        url = reverse("account:login")

        # Test page by GET response
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountLoginView.as_view().__name__)

        # Test page by authorized user GET response
        self.client.login(username="test", password="test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.logout()

    def test_login_post(self):
        user = User.objects.create_user(username="testUser", email="testEmail@gmail.com", password="testPassword")
        url = reverse("account:login")

        response = self.client.post(url, {"username": "testUser", "password": "wrongPassword"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {"username": "testUser", "password": "testPassword"})
        self.assertEqual(response.status_code, 200)

        user.is_active = True
        user.save()

        response = self.client.post(url, {"username": "testUser", "password": "testPassword"})
        self.assertEqual(response.status_code, 302)

    def test_login_form(self):
        user = User.objects.create_user(username="testUser", email="testEmail@gmail.com", password="testPassword")

        # Test is user active
        form = AccountLoginForm(data={"username": "testUser", "password": "testPassword"})
        self.assertTrue(form.has_error('__all__'))

        user.is_active = True
        user.save()

        # Test wrong password
        form = AccountLoginForm(data={"username": "testUser", "password": "wrongPassword"})
        self.assertTrue(form.has_error('__all__'))

        # Test authenticate
        form = AccountLoginForm(data={"username": "testUser", "password": "testPassword"})
        self.assertFalse(form.has_error('__all__'))

    def test_change_password(self):
        url = reverse("account:password_change")
        self.client.login(username="test", password="test")

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountChangePasswordView.as_view().__name__)

        # Test password change
        response = self.client.post(url,
                                    {"old_password": "test", "new_password1": "admin123", "new_password2": "admin123"})
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db(fields=["password"])
        self.assertTrue(self.user.check_password("admin123"))

    def test_change_password_form(self):
        # Test for wrong old password
        form = UserPasswordChangeForm(user=self.user, data={"old_password": "wrong_pass", "new_password1": "admin123",
                                                            "new_password2": "admin123"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('old_password'))

        # Test for new passwords dont match
        form = UserPasswordChangeForm(user=self.user, data={"old_password": "test", "new_password1": "admin12",
                                                            "new_password2": "admin123"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('new_password2'))

        # Test for short password
        form = UserPasswordChangeForm(user=self.user,
                                      data={"old_password": "test", "new_password1": "123", "new_password2": "123"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('new_password2'))

        # Test for too big password
        form = UserPasswordChangeForm(user=self.user, data={"old_password": "test",
                                                            "new_password1": "checkpasscheckpasswordcheckpasswordcheckpasswordcheckpasswordcheckpasswordword",
                                                            "new_password2": "checkpasscheckpasswordcheckpasswordcheckpasswordcheckpasswordcheckpasswordword"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('new_password2'))

    def test_profile(self):
        url = reverse("account:profile")
        self.client.login(username="test", password="test")

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountProfileView.as_view().__name__)

        # Test GET request
        response = self.client.post(url, data={"email": "dolyaanton2@gmail.com"})
        self.assertEqual(response.status_code, 302)

    def test_profile_form(self):
        User.objects.create_user(username="test2", email="test2@gmail.com", password="test2")

        # Test for same email
        form = AccountUpdateForm(user=self.user, instance=self.user, initial={"email": self.user.email},
                                 data={"email": self.user.email})
        self.assertTrue(form.is_valid())

        # Test for new email
        form = AccountUpdateForm(user=self.user, instance=self.user, initial={"email": self.user.email},
                                 data={"email": "testing@gmail.com"})
        self.assertTrue(form.is_valid())

        # Test for used email
        form = AccountUpdateForm(user=self.user, instance=self.user, initial={"email": self.user.email},
                                 data={"email": "test2@gmail.com"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("email"))

    def test_subscribers(self):
        url = reverse("account:subscribes")
        self.client.login(username="test", password="test")

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountSubscribersView.as_view().__name__)

        # Test POST request invalid subscriber
        response = self.client.post(url, data={"slug": "test"})
        self.assertEqual(response.status_code, 404)

        # Test POST request valid subscriber
        anime = Anime.objects.create(name="test", poster=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        Subscribe.objects.create(anime=anime, user=self.user)
        response = self.client.post(url, data={"slug": "test"})
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        url = reverse("account:register")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountRegisterView.as_view().__name__)

        self.client.login(username="test", password="test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.logout()

        response = self.client.post(url, data={"username": "test2",
                                               "email": "test2@gmail.com",
                                               "password1": "testing2",
                                               "password2": "testing2"
                                               })

        self.assertTemplateUsed(response, "account/registered.jinja")

    def test_register_form(self):
        # Test for different passwords
        form = UserCreationForm(data={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "123",
            "password2": "321"
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__'))

        # Test for short password
        form = UserCreationForm(data={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "123",
            "password2": "123"
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__'))

        # Test for long password
        form = UserCreationForm(data={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "lewkrjwlekrlewkrjwlekrjwlerkjlewkrjwlekrjwlerkjjwlerkjwelkrjwelrhwjkewlqkrj",
            "password2": "lewkrjwlekrlewkrjwlekrjwlerkjlewkrjwlekrjwlerkjjwlerkjwelkrjwelrhwjkewlqkrj"
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__'))

        # Test password same as email or nickname
        form = UserCreationForm(data={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password1": "testuser",
            "password2": "testuser"
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__'))

        # Test username already in use
        form = UserCreationForm(data={
            "username": "test",
            "email": "testuser@gmail.com",
            "password1": "hellopassword",
            "password2": "hellopassword"
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__'))

        # Test user already registered but not activated
        User.objects.create_user(username="un_active_user", email="un_active_user@gmail.com", password="un_active_user")
        form = UserCreationForm(data={
            "username": "un_active_user",
            "email": "testuser@gmail.com",
            "password1": "hellopassword",
            "password2": "hellopassword"
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__'))

        # Test user creation
        form = UserCreationForm(data={
            "username": "register_user",
            "email": "register_user@gmail.com",
            "password1": "hellopassword",
            "password2": "hellopassword"
        })

        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_error('__all__'))
        self.assertEqual(form.save(True).username, "register_user")

    def test_validate_email(self):
        user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="testuser")
        token = generator.make_token(user)

        # Test wrong token
        response = self.client.get(reverse("account:verify", kwargs={"username": "testuser", "token": "wrong_token"}))
        self.assertEqual(response.status_code, 404)

        # Test validation
        response = self.client.get(reverse("account:verify", kwargs={"username": "testuser", "token": token}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ValidateEmailView.as_view().__name__)

        user.refresh_from_db()

        # Test verify attempt at active account
        response = self.client.get(reverse("account:verify", kwargs={"username": "testuser", "token": token}))
        self.assertEqual(response.status_code, 302)

        # Test verify attempt while logged in
        self.client.login(username="testuser", password="testuser")
        response = self.client.get(reverse("account:verify", kwargs={"username": "testuser", "token": token}))
        self.assertEqual(response.status_code, 302)

    def test_validate_email_change(self):
        email = "testmail@gmail.com"
        token = salted_hmac(
            self.user.pk,
            f"{self.user.email}{email}",
            secret=settings.SECRET_KEY,
            algorithm='sha1'
        ).hexdigest()[::2]

        self.client.login(username="test", password="test")

        # Test wrong token
        response = self.client.get(reverse("account:change_email", kwargs={"email": email, "token": "wrong_token"}))
        self.assertEqual(response.status_code, 404)

        # Test sending token
        response = self.client.get(reverse("account:change_email", kwargs={"email": email, "token": token}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func.__name__, AccountEmailChangeView.as_view().__name__)

    def test_account_reset(self):
        url = reverse("account:reset")

        # Test GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountResetView.as_view().__name__)

        # Test logged in GET request
        self.client.login(username="test", password="test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.logout()

        # Test POST request
        response = self.client.post(url, data={"email": "test@gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/reset_sent.jinja")

    def test_account_reset_confirm(self):
        # Test logged in GET request
        self.client.login(username="test", password="test")
        response = self.client.get(
            reverse("account:reset_confirm", kwargs={"email": "test@gmail.com", "token": "randomToken"}))
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        self.user.refresh_from_db()
        token = generator.make_token(self.user)

        # Test GET request
        response = self.client.get(reverse("account:reset_confirm", kwargs={"email": "test@gmail.com", "token": token}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AccountResetConfirmView.as_view().__name__)

        # Test wrong token
        response = self.client.get(
            reverse("account:reset_confirm", kwargs={"email": "test@gmail.com", "token": "wrong_token"}))
        self.assertEqual(response.status_code, 404)

        # Test wrong token
        response = self.client.get(
            reverse("account:reset_confirm", kwargs={"email": "wrong_mail@gmail.com", "token": token}))
        self.assertEqual(response.status_code, 404)

        # Test post request
        response = self.client.post(
            path=reverse("account:reset_confirm", kwargs={"email": "test@gmail.com", "token": token}),
            data={"password1": "newpassword123", "password2": "newpassword123"})
        self.assertEqual(response.status_code, 302)

    def test_account_reset_confirm_form(self):
        # Test passwords don't match
        form = AccountResetConfirmForm(user=self.user, data={"password1": "123", "password2": "321"})
        self.assertFalse(form.is_valid())

        # Test for short password
        form = AccountResetConfirmForm(user=self.user, data={"password1": "123", "password2": "123"})
        self.assertFalse(form.is_valid())

        # Test for long password
        form = AccountResetConfirmForm(user=self.user, data={
            "password1": "rtghjejghlwkjhrlkjewhrlwekjrhwkjerhlkwjehrlwkjewrjhwekrhdqweqweqweqweqewqwe",
            "password2": "rtghjejghlwkjhrlkjewhrlwekjrhwkjerhlkwjehrlwkjewrjhwekrhdqweqweqweqweqewqwe"
        })
        self.assertFalse(form.is_valid())

        # Test for password same as email or nickname
        form = AccountResetConfirmForm(user=self.user, data={"password1": "test@gmail.com",
                                                             "password2": "test@gmail.com"})
        self.assertFalse(form.is_valid())

        # Test password change
        form = AccountResetConfirmForm(user=self.user, data={"password1": "newTestPassword",
                                                             "password2": "newTestPassword"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password1'], "newTestPassword")


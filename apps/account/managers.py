from django.contrib.auth.base_user import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, username, email, is_active=False, password=None):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):

        user = self.create_user(
            username,
            email,
            is_active=True,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
import django.contrib.auth.password_validation as password_validators
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_auth.serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.exceptions import (
    EmailRegisteredNotVerifiedException,
    EmailToResetNotExistException,
    EmailValidateError,
    LogInException,
    MissedUsernameOrEmailException,
    PasswordException,
    PasswordsNotMatchException,
    PasswordValidateError,
    UserAccountDisabledException,
    UsernameRegisteredWithThisEmailException,
    UserNotExistsException,
)
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        write_only=True,
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    last_name = serializers.CharField(
        write_only=True,
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "name")

    def validate_email(self, email):
        user = self.context["request"].user

        if email.strip() == "":
            raise MissedUsernameOrEmailException()

        try:
            validate_email(email)
        except ValidationError as error:
            raise EmailValidateError(error.messages[0])

        if User.objects.filter(email__iexact=email.lower()).exclude(pk=user.pk).exists():
            raise UsernameRegisteredWithThisEmailException()

        return email

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    email = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    @classmethod
    def validate_email(cls, email):
        if email.strip() == "":
            raise MissedUsernameOrEmailException()
        try:
            validate_email(email)
        except ValidationError as error:
            raise EmailValidateError(error.messages[0])

        is_registered = User.objects.filter(email__iexact=email.lower()).exists()
        if is_registered:
            raise UsernameRegisteredWithThisEmailException()

        return email

    @classmethod
    def validate_password1(cls, password):
        try:
            password_validators.validate_password(password)
        except ValidationError as error:
            raise PasswordValidateError(error.messages[0])
        return password

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise PasswordsNotMatchException()
        user = User(
            password=data["password1"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
        )
        validate_password(data["password1"], user)
        return data

    def get_cleaned_data(self):
        clean_data = {
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name"),
            "last_name": self.validated_data.get("last_name", ""),
        }
        return clean_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

    def custom_signup(self, request, user):
        pass


class UserLoginSerializer(LoginSerializer):
    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            raise LogInException("Incorrect email or password.")

        return user

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            raise LogInException("Incorrect username or password.")

        return user

    def _validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            raise LogInException()

        return user

    def validate(self, attrs):
        username = attrs.get("username", None)
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        user = None

        if "allauth" in settings.INSTALLED_APPS:
            # Authentication through email
            if settings.ACCOUNT_AUTHENTICATION_METHOD == settings.ACCOUNT_AUTHENTICATION_METHOD_EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif settings.ACCOUNT_AUTHENTICATION_METHOD == settings.ACCOUNT_AUTHENTICATION_METHOD_USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                username = User.objects.get(email=email)

            if username:
                user = self._validate_username_email(username, "", password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                raise UserAccountDisabledException()
        else:
            raise LogInException("Unable to log in with provided credentials.")

        # If required, is the email verified?
        if "rest_auth.registration" in settings.INSTALLED_APPS:
            if settings.ACCOUNT_EMAIL_VERIFICATION == settings.ACCOUNT_EMAIL_VERIFICATION_MANDATORY:
                email_address = user.emailaddress_set.filter(email=user.email).first()
                if not (email_address and email_address.verified):
                    raise EmailRegisteredNotVerifiedException()

        attrs["user"] = user
        return attrs


class UserPasswordChangeSerializer(PasswordChangeSerializer):
    old_password = serializers.CharField(max_length=128, allow_blank=True)
    new_password1 = serializers.CharField(max_length=128, allow_blank=True)
    new_password2 = serializers.CharField(max_length=128, allow_blank=True)

    def validate(self, attrs):
        password = attrs.get("new_password1")
        old_password = attrs.get("old_password")
        try:
            password_validators.validate_password(password)
        except ValidationError as error:
            raise PasswordValidateError(error.messages[0])
        if old_password == password:
            raise PasswordException(message="Old password and new password can not be the same")
        attrs = super().validate(attrs)
        return attrs

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            raise PasswordException()
        return value


class UserTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_user(cls, user_id: str) -> User:
        try:
            return User.objects.get(pk=user_id)
        except Exception:
            raise UserNotExistsException()

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        # check exist user
        user_id = refresh.payload.get("id", None)
        self.get_user(user_id=user_id)

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)
            access = refresh.access_token
            expire = access.current_time + access.lifetime
            data["expire"] = int(expire.timestamp())

        return data


class ResponseTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    expire = serializers.CharField(read_only=True)


class UserLoginBodySerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ResponseChangePasswordSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)

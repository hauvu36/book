from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def respond_email_verification_sent(self, request, user):
        """
        We don't need this redirect.
        """
        pass

    def save_user(self, request, user, form, commit=True):
        # Get other custom field in data
        # data = form.cleaned_data
        user = super().save_user(request, user, form, commit)
        return user

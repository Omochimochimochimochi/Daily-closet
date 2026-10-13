
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password


class CustomSetPasswordForm(SetPasswordForm):
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password1')

        if password:
            validate_password(password, self.user)

        return cleaned_data

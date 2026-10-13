
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordLettersAndNumbersValidator:

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                "パスワードは8文字以上で入力してください。"
            )

        if not re.search(r"[A-Za-z]", password):
            raise ValidationError(
                "パスワードには英字を含めてください。"
            )

        if not re.search(r"[0-9]", password):
            raise ValidationError(
                "パスワードには数字を含めてください。"
            )

    def get_help_text(self):
        return "パスワードは英字と数字を含む8文字以上で入力してください。"

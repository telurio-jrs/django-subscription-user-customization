from db.library.utils.validator import Validator
from db.models import User
from django import forms
from django.core.exceptions import ValidationError


class IndexForm(forms.ModelForm, Validator):
    class Meta:
        model = User
        fields = ['use_login', 'use_password']

    def clean(self):
        use_login = self.cleaned_data.get('use_login')
        use_password = self.cleaned_data.get('use_password')

        user = User.objects.get_user(
            useremail=use_login,
            userpassword=use_password,
        )
        if not user:
            raise ValidationError(message='Incorrect email or password.')
        else:
            if not user.get('use_is_valid'):
                raise ValidationError(
                    message='Your email has not yet been verified, please complete this step before logging in.'  # noqa: E501
                )

    def clean_use_password(self):
        # Password validation according to the business rule applied
        password = self.cleaned_data.get('use_password')

        if self.valid_special_chars(password):
            raise ValidationError(message='invalid')
        return password

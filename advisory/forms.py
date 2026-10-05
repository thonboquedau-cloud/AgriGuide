from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            'name',
            'email',
            'subject',
            'message',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            }),

            'subject': forms.TextInput(attrs={
                'placeholder': 'Enter feedback subject'
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Write your feedback or message...',
                'rows': 6
            }),
        }


class FarmerRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

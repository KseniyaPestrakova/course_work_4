from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Укажите email")
    username = forms.CharField(max_length=50, required=True)
    usable_password = None
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=45, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ник'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите ваше имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите вашу фамилию'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите страну'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'country']

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ник'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите ваше имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите вашу фамилию'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Укажите номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите страну'})

    def clean_email(self):
        """ Проверка уникальности email, исключая текущего пользователя """
        email = self.cleaned_data.get('email')
        user = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).first()
        if user:
            raise forms.ValidationError("Этот email уже используется другим пользователем.")
        return email

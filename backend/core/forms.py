from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    first_name = forms.CharField(max_length=150, label="Nome")
    last_name = forms.CharField(max_length=150, label="Sobrenome")
    campus_id = forms.CharField(max_length=40, required=False, label="Matrícula")
    phone = forms.CharField(max_length=30, required=False, label="Telefone")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "campus_id",
            "phone",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.is_active = True
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.campus_id = self.cleaned_data["campus_id"]
            profile.phone = self.cleaned_data["phone"]
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, label="Nome")
    last_name = forms.CharField(max_length=150, label="Sobrenome")
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "phone", "campus_id")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].initial = self.instance.user.first_name
        self.fields["last_name"].initial = self.instance.user.last_name
        self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.user_id).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save(update_fields=["first_name", "last_name", "email"])
            profile.save()
        return profile


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "title",
            "description",
            "category",
            "location",
            "characteristics",
            "status",
            "image",
            "contact_note",
            "is_public",
        )
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


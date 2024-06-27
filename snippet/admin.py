from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from snippet.models import CustomUser, Snippet
from django import forms

# Register your models here.

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta): # type: ignore
        model = CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # type: ignore
        model = CustomUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class MyUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image', 'birth_date',)}),
    ) # type: ignore

admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Snippet)
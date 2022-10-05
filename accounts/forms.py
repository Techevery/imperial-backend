from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('email',)
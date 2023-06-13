from django.forms import ModelForm
from .models import User

# creates user form based on user model

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'



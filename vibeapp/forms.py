from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Message

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'date_of_birth', 'gender', 'class_10_school', 'class_10_passing_year', 'class_12_school', 'class_12_passing_year', 'college_name', 'expected_graduation_year')
        widgets = {
                    'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
                }
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message...', 'autocomplete': 'off'}),
        }
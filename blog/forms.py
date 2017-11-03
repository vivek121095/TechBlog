from django import forms
from blog.models import Comment,Post,Profile
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','text',)
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text' : forms.Textarea(attrs={'class':'editable'}),
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'editable'})
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')
        year = timezone.now().year
        widgets= {
            'bio' : forms.widgets.Textarea(attrs={'class':'editable'}),
            'birth_date':forms.widgets.SelectDateWidget(years=[years for years in range(1980,year+1)])
        }

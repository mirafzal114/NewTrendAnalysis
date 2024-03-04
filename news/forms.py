from django import forms
from .models import Comment,News
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'body', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
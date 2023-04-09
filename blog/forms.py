from django import forms
from blog.models import Comment
from blog.models import Article


#新規記事投稿
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'author']
        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(),
            'author': forms.TextInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=(
            'comment',
        )
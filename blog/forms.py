from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入您的评论内容...',
                'maxlength': '1000'
            })
        }
        labels = {
            'content': '评论内容'
        }
# posts/forms.py

from django import forms
from .models import Post, Category, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Fieldset, Field


class PostCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Choice category'
    )

    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'image', 'tags')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'category',
            'content',
            'image',
            'tags',
            Submit('submit', 'Опубликовать (Ожидание модерации)',
                   css_class='btn btn-primary mt-3')
        )
        self.helper.enctype = 'multipart/form-data'
        self.helper.form_tag = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment here'})
        }


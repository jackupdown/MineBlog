from django import forms
from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError
from home import models


class ArticleForm(Form):
    title = fields.CharField(
        required=True,
        max_length=128,
        error_messages={
            'required': '标题不能为空',
            'max_length': '标题最大长度128',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control thirty-width', 'placeholder': '请输入文章标题'})
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'placeholder': '请输入文章内容'})
    )
    type = fields.ChoiceField(
        widget=widgets.Select(attrs={'class': 'form-control thirty-width'})
    )
    category = fields.ChoiceField(
        widget=widgets.Select(attrs={'class': 'form-control thirty-width'})
    )
    tags = fields.MultipleChoiceField(
        required=False,
        widget=widgets.CheckboxSelectMultiple()
    )

    # 通过重写__init__方法来动态获取文章类型及标签等信息
    def __init__(self, blogId, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['type'].choices = models.Article.typeChoice
        self.fields['category'].choices = models.Category.objects.filter(blog_id=blogId).values_list('nid', 'title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blogId).values_list('nid', 'title')


class ArticleFormTwo(Form):
    title = fields.CharField(
        required=True,
        max_length=128,
        error_messages={
            'required': '标题不能为空',
            'max_length': '标题最大长度128',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control thirty-width', 'placeholder': '请输入文章标题'})
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'placeholder': '请输入文章内容'})
    )
    type = fields.ChoiceField(
        required=False,
        widget=widgets.Select(attrs={'class': 'form-control thirty-width'})
    )
    category = fields.ChoiceField(
        required=False,
        widget=widgets.Select(attrs={'class': 'form-control thirty-width'})
    )
    tags = fields.MultipleChoiceField(
        required=False,
        widget=widgets.CheckboxSelectMultiple()
    )

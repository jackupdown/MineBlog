from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError
from home import models


class LoginForm(Form):
    """登陆表单"""
    user = fields.CharField(
        required=True,
        min_length=3,
        max_length=32,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名至少3位',
            'max_length': '用户名最多32位',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名', 'name': 'user'}),
    )
    pwd = fields.CharField(
        required=True,
        min_length=8,
        max_length=64,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少8位',
            'max_length': '密码最多64位',
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码', 'name': 'pwd'}),
    )
    code = fields.CharField(
        required=True,
        min_length=5,
        max_length=5,
        error_messages={
            'required': '验证码不能为空',
            'min_length': '请输入完整的5位验证码',
            'max_length': '请输入完整的5位验证码',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '验证码', 'name': 'code'}),
    )


class RegisterForm(Form):
    """注册表单"""
    userName = fields.SlugField(
        required=True,
        min_length=3,
        max_length=32,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名至少3位',
            'max_length': '用户名最多32位',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名', 'name': 'userName'}),
    )
    password1 = fields.CharField(
        required=True,
        min_length=8,
        max_length=64,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少8位',
            'max_length': '密码最多64位',
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码', 'name': 'password1'}),
    )
    password = fields.CharField(
        required=True,
        min_length=8,
        max_length=64,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少8位',
            'max_length': '密码最多64位',
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码', 'name': 'password2'}),
    )
    nickName = fields.CharField(
        required=True,
        max_length=32,
        error_messages={
            'required': '昵称不能为空',
            'max_length': '昵称最多32位',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '昵称', 'name': 'nickName'}),
    )
    email = fields.EmailField(
        required=True,
        max_length=64,
        error_messages={
            'required': '邮箱不能为空',
            'max_length': '邮箱最多64位',
            'invalid': '邮箱格式错误',
        },
        widget=widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱', 'name': 'email'})
    )
    code = fields.CharField(
        required=True,
        min_length=5,
        max_length=5,
        error_messages={
            'required': '验证码不能为空',
            'min_length': '请输入完整的5位验证码',
            'max_length': '请输入完整的5位验证码',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '验证码', 'name': 'code'}),
    )
    avatar = fields.CharField(required=False)

    def clean_userName(self):
        """
        用户名是否已存在确认
        :return:
        """
        userName = self.cleaned_data.get('userName')
        if models.UserInfo.objects.filter(userName=userName):
            raise ValidationError('该用户名已存在！')
        return userName

    def clean_email(self):
        """
        邮箱是否已存在确认
        :return:
        """
        email = self.cleaned_data.get('email')
        if models.UserInfo.objects.filter(email=email):
            raise ValidationError('该邮箱已存在！')
        return email

    def clean_password(self):
        """
        密码是否一致确认
        :return:
        """
        pwd1 = self.cleaned_data.get('password1')
        pwd = self.cleaned_data.get('password')
        if pwd1 and pwd and pwd1 != pwd:
            raise ValidationError('密码不一致，请检查！')
        return pwd


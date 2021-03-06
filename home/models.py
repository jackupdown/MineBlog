from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    userName = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickName = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像')
    createTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝', to='UserInfo', through='UserFans',
                                  related_name='f', through_fields=('user', 'follower'))

    def __str__(self):
        return self.userName


class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='follower')

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    文章标签
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=128)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    """
    文章标签关系表
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        return self.article.title


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')

    def __str__(self):
        return self.article.title


class Article(models.Model):
    """
    文章信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    createTime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    readCount = models.IntegerField(verbose_name='阅读数', default=0)
    commentCount = models.IntegerField(verbose_name='评论数', default=0)
    upCount = models.IntegerField(verbose_name='点赞数', default=0)
    downCount = models.IntegerField(verbose_name='踩数', default=0)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', null=True)
    category = models.ForeignKey(verbose_name='所属分类', to='Category', to_field='nid', blank=True, null=True, default=None)
    typeChoice = [
        (1, 'Python'),
        (2, 'Linux'),
        (3, 'OpenStack'),
        (4, 'GoLang'),
    ]
    articleTypeId = models.IntegerField(choices=typeChoice, default=None)
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    def __str__(self):
        return self.title


class UpDown(models.Model):
    """
    文章赞或者踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='赞或者踩的用户', to='UserInfo', to_field='nid')
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    createTime = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', blank=True, null=True, default=None)
    article = models.ForeignKey(verbose_name='被评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')

    def __str__(self):
        return self.content

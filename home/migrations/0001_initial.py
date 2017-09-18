# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-10 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('summary', models.CharField(max_length=255, verbose_name='文章简介')),
                ('readCount', models.IntegerField(default=0, verbose_name='阅读数')),
                ('commentCount', models.IntegerField(default=0, verbose_name='评论数')),
                ('upCount', models.IntegerField(default=0, verbose_name='点赞数')),
                ('downCount', models.IntegerField(default=0, verbose_name='踩数')),
                ('articleTypeId', models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, 'OpenStack'), (4, 'GoLang')], default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Article', verbose_name='所属文章')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('site', models.CharField(max_length=32, unique=True, verbose_name='个人博客前缀')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主题')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Article', verbose_name='被评论文章')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back', to='home.Comment', verbose_name='回复评论')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='标签名称')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='UpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.BooleanField(verbose_name='是否赞')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('nickName', models.CharField(max_length=32, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('avatar', models.ImageField(upload_to='', verbose_name='头像')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('fans', models.ManyToManyField(related_name='f', through='home.UserFans', to='home.UserInfo', verbose_name='粉丝')),
            ],
        ),
        migrations.AddField(
            model_name='userfans',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='home.UserInfo', verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='home.UserInfo', verbose_name='博主'),
        ),
        migrations.AddField(
            model_name='updown',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.UserInfo', verbose_name='赞或者踩的用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.UserInfo', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.UserInfo'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Category', verbose_name='所属分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='home.Article2Tag', to='home.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([('user', 'follower')]),
        ),
        migrations.AlterUniqueTogether(
            name='updown',
            unique_together=set([('article', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
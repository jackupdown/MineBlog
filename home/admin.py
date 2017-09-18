from django.contrib import admin
from .models import UserInfo, UpDown, UserFans, Article, Article2Tag, ArticleDetail, Category, Tag, Comment, Blog


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('userName', 'nickName', 'email', 'createTime')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'site', 'theme', 'user')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'blog', 'articleTypeId')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'content', 'reply')

admin.site.register([UpDown, UserFans, Article2Tag, ArticleDetail, Category, Tag])

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)


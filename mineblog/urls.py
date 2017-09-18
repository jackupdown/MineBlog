"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from home import views as homeViews
from backend import views as backendViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homeViews.index), # 网站主页
    url(r'^(\w+)/(?P<type_id>\d+)/', homeViews.index),    # 文章分类
    url(r'^article/(\w+)/(?P<type_id>\d+)/', homeViews.index),    # 网站主页分页
    url(r'^(\w+)/article/(\d+).html', homeViews.home),    # 个人主页分页
    url(r'^login/', homeViews.login),    # 登陆
    url(r'^check-code/', homeViews.check_code),      # 获取验证码
    url(r'^logout/', homeViews.logout),  # 登出
    url(r'^register/', homeViews.register),  # 注册
    url(r'^upload_avatar/', homeViews.upload_avatar),  # 上传头像
    url(r'^u/(?P<site>\w+)/(?P<type>\w*)/(?P<kind>\w*-*\w*)', homeViews.home),  # 用户博客主页
    url(r'^u/(?P<userName>\w+)/info.html$', homeViews.userInfo),  # 用户个人信息页
    url(r'^thumb/', homeViews.thumb),  # 赞或者踩
    url(r'^postComment/', homeViews.postComment),  # 发表文章评论
    url(r'^delComment/', homeViews.delComment),  # 删除文章评论
    url(r'^fans/', homeViews.fans),  # 关注或取消关注

    url(r'^backend/', backendViews.backend),  # 后台管理
    url(r'^article-(?P<articleTypeId>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+).html$', backendViews.articleFilter),  # 筛选文章
    url(r'^article/add/', backendViews.articleAdd),  # 新建文章
    url(r'^article/edit/', backendViews.articleEdit),  # 编辑文章
    url(r'^article/del/', backendViews.articleDel),  # 删除文章
    url(r'^upload.html$', backendViews.upload),  # KindEditor上传文件

]

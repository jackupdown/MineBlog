from django.shortcuts import render, HttpResponse, redirect
from utils.pagnition import PageInfo
from utils.random_check_code import rd_check_code
from django.db import connection, transaction
from django.db.models import Count, F
from home import models
from home import forms
from io import BytesIO
import os
import json
import datetime


def index(request, *args, **kwargs):
    """
    网站主页，分页、分类展示所有文章，并提供阅读、点赞和评论排行文章列表
    :param request:
    :return:
    """
    user = request.session.get('user', None)    # 从session中获取当前登陆用户，若无，则user=None
    if user:
        user = models.UserInfo.objects.filter(userName=user).first()    # 根据用户名获取数据库中的user对象
    condition = {}  # 查表条件——文章类型
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else 0    # 获取文章固定分类id
    if type_id:
        condition['articleTypeId'] = type_id
    type_choice_list = models.Article.typeChoice     # 获取文章固定分类
    type_url = 'all'    # 分页url
    for i in type_choice_list:  # 获得文章固定分类id对应的类型
        if type_id in i:
            type_url = i[1]

    all_count = models.Article.objects.filter(**condition).count()  # 获取对应分类的文章总数
    page_info = PageInfo(current_page=request.GET.get('page'),
                         all_count=all_count,
                         base_url='/article/%s/%s' % (type_url, type_id),
                         per_page=5)
    article_list = models.Article.objects.filter(**condition).order_by('-nid')[page_info.start_data(): page_info.end_data()]     # 文章显示数（按时间降序）
    read_ordering = models.Article.objects.order_by('-readCount')[0:5]      # 阅读排行——取前5，以下相同
    up_ordering = models.Article.objects.order_by('-upCount')[0:5]       # 点赞排行
    comment_ordering = models.Article.objects.order_by('-commentCount')[0:5]         # 评论排行
    return render(request, 'index.html',
                  {'user': user, 'type_choice_list': type_choice_list, 'type_id': type_id, 'article_list': article_list,
                   'readOrdering': read_ordering, 'upOrdering': up_ordering, 'commentOrdering': comment_ordering,
                   'page_info': page_info,
                   })


def home(request, *args, **kwargs):
    """
    用户个人主页
    :param request:
    :param args:
    :param kwargs: site,type,kind
    :return:
    """
    page_info = None        # 分页
    article_list = None     # 文章列表
    article_info = None     # 博文
    upDown = None           # 赞踩
    comment_list = None     # 评论
    comm = None             # 多级评论
    nextArticle = None      # 下一篇博文
    preArticle = None       # 上一篇博文
    loginUserObj = models.UserInfo.objects.filter(userName=request.session.get('user')).first()     # 登陆用户

    if request.path_info.endswith('html'):  # 博文详情页
        site = args[0]      # 博客地址后缀
        article_id = int(args[1])   # 博文id
        blog_info = models.Blog.objects.filter(site=site).first()   # 当前博主的blog对象
        article_info = models.Article.objects.filter(nid=article_id).first()    # 文章详情对象
        upDown = models.UpDown.objects.filter(article=article_id, user=loginUserObj).first()    # 赞、踩情况
        nextArticle = models.Article.objects.filter(nid=article_id+1).first()   # 下一篇文章
        preArticle = models.Article.objects.filter(nid=article_id-1).first()    # 上一篇文章

        # 文章评论列表
        comments = models.Comment.objects.filter(article=article_id).values\
            ('nid', 'content', 'createTime', 'reply', 'article', 'user__blog__site', 'user__userName', 'user__nickName')
        comments_list = []
        for row in comments:
            d = {'id': row['nid'], 'content': row['content'], 'createTime': str(row['createTime']), 'nickName': row['user__nickName'],
                 'user': row['user__userName'], 'site': (row['user__blog__site'] if row['user__blog__site'] else 0),
                 'reply': (row['reply'] if row['reply'] else 0), 'child': []}
            comments_list.append(d)
        comments_dic = {}
        for item in comments_list:
            comments_dic[item['id']] = item
        ret_list = []
        [comments_dic[item['reply']]['child'].append(item) if item['reply'] else ret_list.append(item) for item in
         comments_list]

        # 递归生成多级评论的数据结构
        def comments(li, i=0):
            tab = '  ' * i
            for item in li:
                print(tab, item['content'])
                if item['child']:
                    comments(item['child'], i+1)
        comments(ret_list)

        comm = ret_list
        print(comm)
    else:   # 个人博客主页
        site = kwargs['site']  # 当前博主site
        article_type = kwargs['type'] + '__title'   # 文章查找类别，只对tags和category有效
        kind = kwargs['kind']   # 文章的具体类别
        blog_info = models.Blog.objects.filter(site=site).first()   # 当前博主的blog对象
        if kwargs['type'] == 'blog':    # 博主全部文章
            dic = {'blog': blog_info}   # 查询条件
        elif kwargs['type'] == 'date':  # 按日期分类的文章
            date = kwargs['kind']   # 获取指定日期
            date = date.split('-')
            year = date[0]
            month = date[1]
            date_from = datetime.datetime(int(year), int(month), 1, 0, 0)   # 起始月份
            date_to = datetime.datetime(int(year), int(month)+1, 1, 0, 0)   # 结束月份
            dic = {'blog': blog_info, 'createTime__range': (date_from, date_to)}
        else:  # 按tag或category分类的文章
            if kind == 'None':
                dic = {'blog': blog_info, article_type: None}   # 无tags或category分类的文章
            else:
                dic = {'blog': blog_info, article_type: kind}   # 按照tags或category分类的文章

        # 分页获取内容
        all_count = models.Article.objects.filter(**dic).count()  # 获取对应分类的文章总数
        page_info = PageInfo(current_page=request.GET.get('page'),
                             all_count=all_count,
                             base_url='/u/%s/%s/%s/' % (site, kwargs['type'], kwargs['kind']),
                             per_page=5)
        article_list = models.Article.objects.filter(**dic).order_by('-nid')[page_info.start_data(): page_info.end_data()]  # 文章显示数

    # 粉丝及关注信息
    user_info = {}  # 用户粉丝及关注信息
    fans = models.UserFans.objects.filter(user=blog_info.user).count()  # 粉丝
    followers = models.UserFans.objects.filter(follower=blog_info.user).count()     # 关注者
    user_info['fans'] = fans    # 当前用户的粉丝数
    user_info['followers'] = followers  # 当前用户关注的人数

    # 文章标签及文章个数
    tags_list = models.Article.objects.filter(blog=blog_info).values('tags', 'tags__title').annotate(c=Count('nid'))

    # 文章分类及文章个数
    category_list = models.Article.objects.filter(blog=blog_info).values('category', 'category__title').annotate(c=Count('nid'))

    # 按月份分类文章并统计个数
    # select = {'month': connection.ops.date_trunc_sql('month', 'createTime')}
    # select = {"month": "date_format(createTime, '%%Y-%%m')"}  # MySQL可用
    select = {"month": "strftime('%%Y-%%m', createTime)"}  # MSQlite可用
    month_list = models.Article.objects.filter(blog=blog_info).extra(select=select).values('month').annotate(number=Count('nid'))
    return render(request,
                  'home.html',
                  {'loginUserObj': loginUserObj, 'blog_info': blog_info, 'user_info': user_info,
                   'article_info': article_info, 'nextArticle': nextArticle, 'preArticle': preArticle,
                   'article_list': article_list, 'page_info': page_info,
                   'tags_list': tags_list, 'month_list': month_list, 'category_list': category_list,
                   'upDown': upDown, 'comment_list': comment_list, 'comments': comm,
                   })


def userInfo(request, *args, **kwargs):
    """
    用户个人信息页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    userName = kwargs.get('userName')
    userInfoObj = models.UserInfo.objects.filter(userName=userName).first()
    return render(request, 'userInfo.html', {'userInfoObj': userInfoObj})


def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        obj = forms.LoginForm()     # 利用Django的form组件生成html表单
        return render(request, 'login.html', {'obj': obj})
    else:
        ret = {'status': True, 'msg': None}
        obj = forms.LoginForm(request.POST)     # post数据form验证
        if obj.is_valid():
            data = obj.cleaned_data
            user = data['user']
            pwd = data['pwd']
            input_code = data['code']
            session_code = request.session.get('code')
            if input_code.upper() == session_code.upper():
                if models.UserInfo.objects.filter(userName=user, password=pwd):
                    request.session['user'] = user
                    v = json.dumps(ret)
                    return HttpResponse(v)
                else:
                    ret['status'] = False
                    ret['msg'] = u'用户名或者密码错误！'
                    v = json.dumps(ret)
                    return HttpResponse(v)
            else:
                ret['status'] = False
                ret['msg'] = u'验证码错误！'
                v = json.dumps(ret)
                return HttpResponse(v)
        else:
            ret['status'] = 'objFalse'
            ret['msg'] = obj.errors
            v = json.dumps(ret)
            return HttpResponse(v)


def check_code(request):
    """
    为用户登陆生成图片验证码
    :param request:
    :return:
    """
    img, code = rd_check_code()     # 调用验证码生成插件
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())      # 以img标签的src属性返回给html页面


def logout(request):
    """
    登出当前用户
    :param request:
    :return:
    """
    request.session.delete(request.session.session_key)
    return redirect('/')


def register(request):
    """
    注册页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        ret = {'status': True, 'msg': None}
        obj = forms.RegisterForm(request.POST)
        if obj.is_valid():
            data = obj.cleaned_data
            data.pop('password1')
            input_code = data.pop('code')
            session_code = request.session.get('code')
            if input_code.upper() == session_code.upper():
                models.UserInfo.objects.create(**data)
                v = json.dumps(ret)
                request.session['user'] = data['userName']
                return HttpResponse(v)
            else:
                ret['status'] = False
                ret['msg'] = {'code': ['验证码错误！']}
                v = json.dumps(ret)
                return HttpResponse(v)
        else:
            ret['status'] = False
            ret['msg'] = obj.errors
            v = json.dumps(ret)
            return HttpResponse(v)


def upload_avatar(request):
    """
    上传用户头像
    :param request:
    :return:
    """
    file_obj = request.FILES.get('avatar')      # 获取上传文件
    file_path = os.path.join('static/images', file_obj.name)    # 存储文件路径拼接
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    ret = {'status': True, 'file_path': file_path}      # 返回服务端的文件路径给浏览器
    v = json.dumps(ret)
    return HttpResponse(v)


def thumb(request):
    """
    点赞，踩
    :param request:
    :return:
    """
    try:
        type = request.GET.get('type')      # 获取用户操作类型
        articleId = int(request.GET.get('article'))     # 获取文章id
        loggerId = int(request.GET.get('loggerId'))     # 获取当前用户id
        with transaction.atomic():
            # 用户赞了这篇文章
            if type == 'up':
                models.UpDown.objects.create(article_id=articleId, user_id=loggerId, up=True)
                models.Article.objects.filter(nid=articleId).update(upCount=F('upCount') + 1)
            # 用户取消赞这篇文章
            elif type == 'undoUp':
                models.UpDown.objects.filter(article_id=articleId, user_id=loggerId).delete()
                models.Article.objects.filter(nid=articleId).update(upCount=F('upCount') - 1)
            # 用户踩了这篇文章
            elif type == 'down':
                models.UpDown.objects.create(article_id=articleId, user_id=loggerId, up=False)
                models.Article.objects.filter(nid=articleId).update(downCount=F('downCount') + 1)
            # 用户取消踩这篇文章
            else:
                models.UpDown.objects.filter(article_id=articleId, user_id=loggerId).delete()
                models.Article.objects.filter(nid=articleId).update(downCount=F('downCount') - 1)
    except Exception as e:
        ret = {'status': 'false', 'msg': str(e)}
        v = json.dumps(ret)
        return HttpResponse(v)

    obj = models.Article.objects.filter(nid=articleId).first()
    ret = {'status': 'true', 'upThumb': obj.upCount, 'downThumb': obj.downCount}    # 将当前用户对该文章的赞踩情况及该文章的赞踩总数返回
    v = json.dumps(ret)
    return HttpResponse(v)


def postComment(request):
    """
    对文章发表评论
    :param request:
    :return:
    """
    articleId = int(request.POST.get('articleId'))   # 被评论文章id
    if request.POST.get('replyId'):
        replyId = int(request.POST.get('replyId'))   # 被回复用户id
    else:
        replyId = None
    commenter = int(request.POST.get('commenter'))   # 评论者id
    comments = request.POST.get('comments')     # 评论内容
    models.Comment.objects.create(article_id=articleId, user_id=commenter, content=comments, reply_id=replyId)
    ret = {'status': True, 'msg': None}
    v = json.dumps(ret)
    return HttpResponse(v)


def delComment(request):
    """
    博主可以删除任何评论，评论者只能删除自己的评论
    为了保持多级评论的队形，只是删除了评论的内容
    :param request:
    :return:
    """
    commentId = request.POST.get('commentId')   # 要删除的评论id
    obj = models.Comment.objects.filter(nid=commentId).first()
    if obj.reply:   # 若该条评论有回复关系，则只删除其内容
        obj.content = '<del>该条评论已被删除！</del>'
        obj.save()
    else:   # 反则，完全删除该条评论
        models.Comment.objects.filter(nid=commentId).delete()
    return HttpResponse('True')


def fans(request):
    """
    关注或取消关注
    :param request:
    :return:
    """
    type = int(request.GET.get('type'))      # 1代表关注，0代表取消关注
    blogerId = int(request.GET.get('blogerId'))     # 博主
    loggerId = int(request.GET.get('loggerId'))     # 登陆用户
    if type:
        models.UserFans.objects.create(user_id=blogerId, follower_id=loggerId)
    else:
        models.UserFans.objects.filter(user=blogerId, follower=loggerId).delete()
    return HttpResponse('success')

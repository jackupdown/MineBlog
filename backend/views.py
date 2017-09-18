from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from backend.forms import ArticleForm
from home import models
from utils.pagnition import PageInfo
from utils.xss import xss
import os, json, re


def backend(request):
    """
    后台管理首页
    :param request:
    :return:
    """
    loginer = request.session.get('user')
    loginerInfo = models.UserInfo.objects.filter(userName=loginer).first()
    articleInfo = models.Article.objects.filter(blog=loginerInfo.blog)
    return render(request, 'backend.html', {'loginerInfo': loginerInfo, 'articleInfo': articleInfo})


def articleFilter(request, **kwargs):
    """
    文章筛选
    :param request:
    :param kwargs:
    :return:
    """
    loginer = request.session.get('user')
    loginerInfo = models.UserInfo.objects.filter(userName=loginer).first()
    condition = {}
    condition['blog_id'] = loginerInfo.blog.nid
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    type_list = models.Article.typeChoice
    category_list = models.Category.objects.filter(blog_id=loginerInfo.blog.nid)
    tag_list = models.Tag.objects.filter(blog_id=loginerInfo.blog)

    all_count = models.Article.objects.filter(**condition).count()  # 获取对应分类的文章总数
    page_info = PageInfo(current_page=request.GET.get('page'),
                         all_count=all_count,
                         base_url='/article-%s-%s-%s.html' % (kwargs['articleTypeId'], kwargs['category_id'], kwargs['tags__nid']),
                         per_page=5)
    article_list = models.Article.objects.filter(**condition)[page_info.start_data(): page_info.end_data()]  # 文章显示数

    return render(request, 'filterArticle.html', {
        'loginerInfo': loginerInfo,
        'type_list': type_list,
        'category_list': category_list,
        'tag_list': tag_list,
        'article_list': article_list,
        'kwargs': kwargs,
        'all_count': all_count,
        'page_info': page_info,
    })


def articleAdd(request):
    """
    添加新文章
    :param request:
    :return:
    """
    loginer = request.session.get('user')
    loginerInfo = models.UserInfo.objects.filter(userName=loginer).first()
    if request.method == 'GET':
        obj = ArticleForm(loginerInfo.blog.nid)
        # 若ArticleForm中未重写init方法，可以通过以下语句动态获取数据库中的文章类型，分类及标签
        # obj.fields['type'].choices = models.Article.typeChoice
        # obj.fields['category'].choices = models.Category.objects.filter(blog=loginerInfo.blog).values_list('nid', 'title')
        # obj.fields['tags'].choices = models.Tag.objects.filter(blog=loginerInfo.blog).values_list('nid', 'title')
        return render(request, 'addArticle.html', {
            'loginerInfo': loginerInfo,
            'obj': obj,
        })
    else:
        obj = ArticleForm(loginerInfo.blog.nid, request.POST)   # 表单验证
        if obj.is_valid():
            data = obj.cleaned_data
            title = data['title']
            articleTypeId = data['type']
            category = data['category']
            tags = data['tags']
            new_content = xss(obj.cleaned_data.get('content'))
            summary = new_content[:200]     # 取文章详细内容的前200个字符作为简介
            article_obj = models.Article.objects.create(
                title=title, summary=summary, blog=loginerInfo.blog, articleTypeId=articleTypeId, category_id=category,
            )
            models.ArticleDetail.objects.create(content=new_content, article=article_obj)
            tag_l = []
            for tag in tags:
                tag_l.append(models.Article2Tag(article=article_obj, tag_id=int(tag)))
            models.Article2Tag.objects.bulk_create(tag_l, 10)
            return redirect('/article-0-0-0.html')
        return render(request, 'addArticle.html', {'obj': obj})


def articleEdit(request):
    """
    编辑文章
    :param request:
    :return:
    """
    articleId = request.GET.get('nid')
    articleObj = models.Article.objects.filter(nid=articleId).first()
    loginer = request.session.get('user')
    loginerInfo = models.UserInfo.objects.filter(userName=loginer).first()
    tagsObj = models.Article2Tag.objects.filter(article_id=articleId).all()
    oldTagsId = [tag.tag_id for tag in tagsObj]
    initial_dic = {
        'title': articleObj.title, 'content': articleObj.articledetail.content, 'type': articleObj.articleTypeId,
        'category': articleObj.category_id, 'tags': oldTagsId}
    if request.method == 'GET':
        obj = ArticleForm(loginerInfo.blog.nid, initial=initial_dic)    # 初始化文章，包含修改前的所有内容
        return render(request, 'editArticle.html', {'loginerInfo': loginerInfo, 'obj': obj, 'articleId': articleId})
    else:
        obj = ArticleForm(loginerInfo.blog.nid, request.POST)
        if obj.is_valid():
            data = obj.cleaned_data
            title = data['title']
            articleTypeId = data['type']
            category = data['category']
            tags = data['tags']
            new_content = xss(obj.cleaned_data.get('content'))
            summary = new_content[:200]
            models.Article.objects.filter(nid=articleId).update(
                title=title, summary=summary, articleTypeId=articleTypeId, category_id=category,
            )
            models.ArticleDetail.objects.filter(article_id=articleId).update(content=new_content)
            newTagsId = []
            for tag in tags:
                newTagsId.append(int(tag))
            addTagsId = list(set(newTagsId).difference(set(oldTagsId)))
            delTagsId = list(set(oldTagsId).difference(set(newTagsId)))
            models.Article2Tag.objects.filter(article_id=articleId, tag_id__in=delTagsId).delete()
            tag_add = []
            for tag in addTagsId:
                tag_add.append(models.Article2Tag(article_id=articleId, tag_id=tag))
            models.Article2Tag.objects.bulk_create(tag_add, 10)
            return redirect('/article-0-0-0.html')
        return render(request, 'editArticle.html', {'obj': obj})


def articleDel(request):
    """
    删除文章
    :param request:
    :return:
    """
    articleId = request.GET.get('articleId')
    models.Article.objects.filter(nid=articleId).delete()
    return HttpResponse('...')


def upload(request):
    """
    KindEditor上传文件
    :param request:
    :return:
    """
    loginer = request.session.get('user')
    if not os.path.isdir(os.path.join('static/images', loginer)):   # 若用户个人文件夹不存在，则创建
        os.makedirs(os.path.join('static/images', loginer))
    file_type = request.GET.get('dir')      # 文件类型
    file_obj = request.FILES.get('imgFile')     # 文件对象
    file_path = os.path.join('static/images', loginer, file_obj.name)   # 上传文件路径
    with open(file_path, 'wb') as f:    # 写文件
        for chunk in file_obj.chunks():
            f.write(chunk)
    dic = {
        'error': 0,
        'url': '/' + file_path,
        'message': '出错了'
    }
    return HttpResponse(json.dumps(dic))

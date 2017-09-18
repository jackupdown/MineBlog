# MineBlog
## 简单模仿博客网站（Django实现）。功能主要有：
* 网站首页展示
* 个人博客首页展示
* 个人博客详情页
* 登陆用户可以对博文进行点赞，多级评论，及关注博主
* 博主能够对博文进行组合筛选
## 技术范畴：
### 自定义插件：
* pagnition，分页插件
* random_check_code，生成图片验证码
* xss，配合kindeditor富文本插件实现后台安全过滤，防止xss攻击
### 数据库：
* sqlite3
* 10张表
* 表关系包含FK&M2M及自关联
### 前端相关：
* Ajax
* 自定义JS字符串的Format方法
```javascript
String.prototype.Format = function (args) {
  /*this代表要调用Format方法的字符串*/
  /*replace的第一个参数为正则表达式，g表示处理匹配到的所有字符串，在js中使用//包起来*/
  /*replace的第二个参数为匹配字符串的处理，k1匹配结果包含{}，k2只保留{}内的内容*/
  var temp = this.replace(/\{(\w+)\}/g, function (k1, k2) {
  /*replace将匹配到的k2用参数args替换后赋给新变量temp*/
        return args[k2];
      });
  /*自定义方法Format将格式化后的字符串返回*/
     return temp;
  }
```
* 通过img标签的src属性动态更新图片验证码
```javascript
function changImg(self) {
    self.src=self.src+"?";
  }
```
* JS递归实现多级评论的展示
```python
# 多级评论数据结构
{'id': 2, 'content': '你的牌打得太溜了！', 'createTime': '2017-07-14 19:35:22.579387', 'nickName': '死亡如风，常伴吾身', 'user': 'jackboy', 'site': 'jackboy', 
'reply': 0, 'child': [{'id': 3, 'content': '楼上休放阙词，扫地僧在此！', 'createTime': '2017-07-14 19:43:03.883001', 'nickName': '龙的传人', 'user': 'LeeSin', 'site': 0, 
'reply': 2, 'child': [{'id': 5, 'content': '本尊来了！', 'createTime': '2017-07-15 16:48:32.144007', 'nickName': '杰克', 'user': 'jack', 'site': 'jack', 
'reply': 3, 'child': [{'id': 13, 'content': 'test1', 'createTime': '2017-07-18 17:18:49.377891', 'nickName': 'smile大盗', 'user': 'smile', 'site': 0, 
'reply': 5, 'child': [{'id': 14, 'content': '<del>该条评论已被删除！</del>', 'createTime': '2017-07-18 17:19:16.784917', 'nickName': '龙的传人', 'user': 'LeeSin', 'site': 0, 
'reply': 13, 'child': []}]}, {'id': 16, 'content': '恭迎圣驾！', 'createTime': '2017-07-18 18:46:14.032889', 'nickName': '龙的传人', 'user': 'LeeSin', 'site': 0, 
'reply': 5, 'child': []}]}]}]}
```
* Bootstrap及FontAwesome美化

## 测试账户
* Admin账户：root；pwd：123456
* 博主账户：jack；pwd：12345678

## 部分页面展示
* 注册页面
![](https://github.com/jackupdown/MineBlog/raw/master/mdPic/register.png)
* 网站首页
![](https://github.com/jackupdown/MineBlog/raw/master/mdPic/home.png)
* 个人首页
![](https://github.com/jackupdown/MineBlog/raw/master/mdPic/phome.png)
* 博文详情页
![](https://github.com/jackupdown/MineBlog/raw/master/mdPic/details.png)
* 多级评论
![](https://github.com/jackupdown/MineBlog/raw/master/mdPic/comments.png)
* 博文筛选
![](https://github.com/jackupdown/MineBlog/raw/master/mdPic/backend.png)


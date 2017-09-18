from bs4 import BeautifulSoup


def xss(old_str):
    """
    kindEditor安全html标签过滤
    :param old_str:
    :return:
    """
    valid_tag = {
        'div': ['class', 'id', 'name', 'style'],
        'a': ['class', 'id', 'name', 'style', 'href', 'target'],
        'p': ['class', 'id', 'name', 'style'],
        'b': ['class', 'id', 'name', 'style'],
        'br': ['class', 'id', 'name', 'style'],
        'strong': ['class', 'id', 'name', 'style'],
        'pre': ['class', 'id', 'name', 'style'],
        'img': ['class', 'id', 'name', 'style', 'src'],
        'span': ['class', 'id', 'name', 'style', 'src'],
        # 'script': ['class', 'id', 'name', 'style', 'src'],    # 一般不允许script标签出现
    }
    soup = BeautifulSoup(old_str, 'html.parser')
    tags = soup.find_all()
    for tag in tags:
        if tag.name not in valid_tag:
            tag.decompose()
        if tag.attrs:
            for k in list(tag.attrs.keys()):
                if k not in valid_tag[tag.name]:
                    del tag.attrs[k]
    new_str = soup.decode()
    return new_str
# coding:utf-8
#mako的定义


# 导入模块
from django.middleware.csrf import get_token
from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse



def render_to_response(request, template, data=None):

    # 定义上下文实例
    context_instance = RequestContext(request)
    # 获取templates地址
    path = settings.TEMPLATES[0]['DIRS'][0]

    # 路径 编码
    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8',
    )

    # 注册template
    mako_template = lookup.get_template(template)


    if not data:
        data = {}

    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)

    result = {}

    for d in context_instance:
        result.update(d)
    result['request'] = request
    request.META["CSRF_COOKIE"] = get_token(request)
    result['csrf_token'] = ('<input type="hidden" id="django-csrf-token"'
                            ' name="csrfmiddlewaretoken" value={0}'
                            ' />'.format(request.META['CSRF_COOKIE']))

    return HttpResponse(mako_template.render(**result))


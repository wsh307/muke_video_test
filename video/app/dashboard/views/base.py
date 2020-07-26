# coding:utf-8
# dashboard 首页

#导入模块
from django.views.generic import View
from app.libs.base_render import render_to_response


class Index(View):

    # dashboard-index视图

    TEMPLATE = 'dashboard/index.html'

    def get(self,request):

        return render_to_response(request, self.TEMPLATE)
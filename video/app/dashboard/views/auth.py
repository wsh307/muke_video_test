# coding:utf-8
# dashboard 登录页

#导入模块
from django.shortcuts import redirect, reverse
from django.views.generic import View
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from app.libs.base_render import render_to_response
from django.core.paginator import Paginator
from app.utils.permission import dashboard_auth





class Login(View):
    #登录视图
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        to = request.GET.get('to','')

        data = {'error':'', 'to':to}

        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        to = request.GET.get('to', '')

        data = {}

        if not username or not password:
            data['error'] = '用户名或密码不得为空'
            return render_to_response(request, self.TEMPLATE, data=data)

        exists = User.objects.filter(username=username).exists()
        if not exists:
            data['error'] = '该用户不存在'
            return render_to_response(request, self.TEMPLATE, data=data)
        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)
        if not user.is_superuser:
            data['error'] = '权限不足，禁止访问'
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request,user)

        if to:

            return redirect(to)

        return redirect(reverse('dashboard_index'))




class AdminManger(View):
    # 管理员视图
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):

        user = User.objects.all()

        #设置分页
        page = request.GET.get('page', 1)
        p = Paginator(user, 10)

        if int(page) <= 1:
            page = 1
        current_page = p.get_page(int(page)).object_list
        total_page = p.num_pages


        data = {'users':current_page, 'total':total_page, 'page_num':int(page)}


        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):
    # 设置管理员状态
    def get(self,request):

        status = request.GET.get('status','on')
        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manger'))


class Logout(View):
    #注销视图
    def get(self,request):

        logout(request)

        return redirect(reverse('dashboard_login'))








# coding:utf-8
# dashboard 视频页

#导入模块
from django.shortcuts import redirect, reverse
from django.views.generic import View
from app.utils.permission import dashboard_auth
from app.libs.base_render import render_to_response
from app.model.video import VideoType,FromType,NationalityType,Video,VideoSub,VideoStar,IdentityType
from app.utils.common import check_and_get_video_type



class ExternaVideo(View):
    # 外链视频
    TEMPLATE = 'dashboard/video/externa_video.html'

    @dashboard_auth
    def get(self, request):

        error = request.GET.get('error','')

        videos = Video.objects.exclude(from_to=FromType.custom.value)

        data = {'error':error, 'videos':videos}

        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):

        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')

        if not all([name, image, video_type, from_to, nationality]):
            return redirect('{0}?error={1}'.format(reverse('externa_video'), '缺少必要信息'))

        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')

        if result.get('code') != 0:
            return redirect('{0}?error={1}'.format(reverse('externa_video'), result['msg']))


        result = check_and_get_video_type(FromType, from_to, '非法的视频来源')
        if result.get('code') != 0:
            return redirect('{0}?error={1}'.format(reverse('externa_video'), result['msg']))


        result = check_and_get_video_type(NationalityType, nationality, '非法的视频地区')
        if result.get('code') != 0:
            return redirect('{0}?error={1}'.format(reverse('externa_video'), result['msg']))


        Video.objects.create(name=name, image=image, info=info,
                             from_to=from_to, video_type=video_type,
                             nationality=nationality)



        return redirect(reverse('externa_video'))


class VideoSubView(View):
    # 视频附属信息
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self,request, video_id):

        data = {}

        error = request.GET.get('error','')

        video = Video.objects.get(pk=video_id)
        data['video'] = video
        data['error'] = error

        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request, video_id):

        url = request.POST.get('url')

        video = Video.objects.get(pk=video_id)
        length = video.video_sub.count()
        if len(url) == 0:
            return redirect('{0}?error={1}'.format(reverse('video_sub', kwargs={'video_id': video_id}), 'url不得为空'))
        try:
            number = length + 1
            VideoSub.objects.create(video=video, url=url, number=number)
        except:
            return redirect('{0}?error={1}'.format(reverse('video_sub', kwargs={'video_id':video_id}), '创建失败'))


        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))


class VideoStarView(View):
    # 演员信息

    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')


        if not all([name, identity, video_id]):
            return redirect('{0}?error={1}'.format(reverse('video_sub', kwargs={'video_id':video_id}),  '缺少必要字段'))

        result = check_and_get_video_type(IdentityType, identity, '非法的身份')
        if result.get('code') != 0:
            return redirect('{0}?error={1}'.format(reverse('video_sub', kwargs={'video_id':video_id}), result['msg']))

        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(video=video, identity=identity, name=name)
        except:
            return redirect('{0}?error={1}'.format(reverse('video_sub', kwargs={'video_id':video_id}), '创建失败'))


        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))


class SterDelete(View):

    def get(self, request,star_id, video_id):

        VideoStar.objects.filter(id=star_id).delete()

        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))







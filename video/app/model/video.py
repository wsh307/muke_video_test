# coding:utf-8
# 视频数据库

from enum import Enum
from django.db import models


class VideoType(Enum):
    # 视频类型
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'

VideoType.movie.label = '电影'
VideoType.cartoon.label = '动漫'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'


class FromType(Enum):
    # 视频来源
    youku = 'youku'
    tx = 'tx'
    custom = 'custom'

FromType.youku.label = '优酷'
FromType.tx.label = '腾讯'
FromType.custom.label = '自制'


class NationalityType(Enum):
    # 地区
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'

NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国'
NationalityType.other.label = '其他'


class IdentityType(Enum):
    hero = 'hero'
    heroine = 'heroine'
    male_supporting_role = 'male_supporting_role'
    female_supporting_role = 'female_supporting_role'
    director = 'director'
    scriptwriter = 'scriptwriter'

IdentityType.hero.label = '男主角'
IdentityType.heroine.label = '女主角'
IdentityType.male_supporting_role.label = '男配角'
IdentityType.female_supporting_role.label = '女配角'
IdentityType.scriptwriter.label = '编剧'
IdentityType.director.label = '导演'


class Video(models.Model):
    # 视频数据表

    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 设置联合索引
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):

        return self.name


class VideoStar(models.Model):
    # 演员信息表

    video = models.ForeignKey(Video, related_name='video_star', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    # 视频地址，集数
    video = models.ForeignKey(Video, related_name='video_sub', on_delete=models.SET_NULL, blank=True, null=True)
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return  'video:{0},number:{1}'.format(self.video, self.number)




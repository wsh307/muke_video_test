# coding:utf-8
# 用户数据库


import hashlib
from django.db import models



def hash_password(password):
    # 加密函数
    if isinstance(password, str):
        password = password.encode('utf-8')

    return hashlib.md5(password).hexdigest().upper()


class ClientUser(models.Model):
    # 用户数据表

    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=500, default='')
    gender = models.CharField(max_length=10, default='')
    birthday = models.DateTimeField(null=False, blank=True, default=None)
    status = models.BooleanField(default=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return "username:{0}".format(self.username)

    @classmethod
    def add(cls, username, password, avatar='', gender='', birthday='', status='', created_time=''):
        # 用户创建函数

        return cls.objects.create(username=username, password=hash_password(password), avatar=avatar, gender=gender,
                                  birthday=birthday, status=status, created_time=created_time)

    @classmethod
    def get_user(cls, username, password):
        # 用户查循函数

        try:
            user = cls.objects.get(username=username, password=password)
            return user
        except:
            return None

    def update_password(self, old_password, new_password):
        # 密码修改函数

        hash_old_password = hash_password(old_password)

        if hash_old_password != self.password:

            return False

        hash_new_password = hash_password(new_password)
        self.password = hash_new_password
        self.save()

        return True

    def update_statue(self):
        # 修改用户状态函数
        self.status = not self.status
        self.save()
        return True
